import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from torch.utils.data import DataLoader, TensorDataset

# Load the processed data
df = pd.read_csv('feature_engineering/processed_engineered_data.csv')

# Convert date_local to datetime
df['date_local'] = pd.to_datetime(df['date_local'])

# Outlier Handling and Log Transformation
target = 'PM2.5 - Local Conditions'
Q1 = df[target].quantile(0.25)
Q3 = df[target].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df[target] >= lower_bound) & (df[target] <= upper_bound)]
df = df.reset_index(drop=True)

# Log transform the target variable
df[target] = np.log1p(df[target])

# Select features
features = ['Region', 'Month', 'Year', 'Carbon monoxide', 'Nitrogen dioxide (NO2)',
            'DayAirTmpAvg (F)', 'DayPrecip (in)',
            'DayRelHumAvg (%)', 'DaySolRadAvg (Ly/day)', 'DayVapPresAvg (mBars)',
            'DayWindRun (MPH)', 'DayWindSpdAvg (MPH)', 'Temp_Range',
            'gis_acres', 'shape__area', 'shape__length', 'duration_days', 'normalized_intensity']

# One-hot encode WindCategory
wind_dummies = pd.get_dummies(df['WindCategory'], prefix='WindCategory')
df = pd.concat([df, wind_dummies], axis=1)
features = features + list(wind_dummies.columns)

# Select target and features
data = df[['date_local', target] + features].copy()
data = data.set_index('date_local')

# Scale the data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# Create sequences
def create_sequences(data, seq_length):
    xs = []
    ys = []
    for i in range(len(data) - seq_length):
        x = data[i:(i + seq_length), 1:]
        y = data[i + seq_length, 0]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

seq_length = 10
X, y = create_sequences(scaled_data, seq_length)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Convert to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

# Create DataLoaders
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=False) #Increase batch size

# LSTM Model (PyTorch) with Dropout
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, dropout_rate):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout_rate)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

input_size = X_train_tensor.shape[2]
hidden_size = 64 #Increase hidden size.
num_layers = 2 #Increase number of layers.
dropout_rate = 0.2 #Add dropout.
model = LSTMModel(input_size, hidden_size, num_layers, dropout_rate)

# Loss and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0005) #Decrease learning rate.

# Train the model
epochs = 100 #Increase epochs.
for epoch in range(epochs):
    model.train() #Set model to train mode.
    for inputs, targets in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

# Make predictions
model.eval()
with torch.no_grad():
    y_pred_tensor = model(X_test_tensor)
    y_pred_scaled = y_pred_tensor.numpy()

# Inverse transform predictions and true values
y_pred_log = scaler.inverse_transform(np.concatenate((y_pred_scaled, np.zeros((y_pred_scaled.shape[0], scaled_data.shape[1] - 1))), axis=1))[:, 0]
y_test_log = scaler.inverse_transform(np.concatenate((y_test_tensor.numpy().reshape(-1,1), np.zeros((y_test_tensor.numpy().reshape(-1,1).shape[0], scaled_data.shape[1] - 1))), axis=1))[:, 0]

#Inverse the log transform.
y_pred = np.expm1(y_pred_log)
y_test = np.expm1(y_test_log)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")
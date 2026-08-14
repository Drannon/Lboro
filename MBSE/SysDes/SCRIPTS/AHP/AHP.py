import numpy as np
import pandas as pd

CSV_FILE = "../../pairwise_matrix.csv"

df = pd.read_csv(CSV_FILE, index_col=0)

# Convert the matrix to array
A = df.to_numpy(dtype=float)

requirements = df.index.tolist()

eigenvalues, eigenvectors = np.linalg.eig(A)

# Principal eigenvalue = largest real eigenvalue
max_index = np.argmax(eigenvalues.real)

lambda_max = eigenvalues[max_index].real

# Corresponding eigenvector
primary_eigenvector = eigenvectors[:, max_index].real

# Eigenvectors can be returned with a negative sign.
# Convert to positive values.
primary_eigenvector = np.abs(primary_eigenvector)

# Normalise so that all weights sum to 1
weights = primary_eigenvector / primary_eigenvector.sum()

# Results
results = pd.DataFrame({
    "Requirement": requirements,
    "Weight": weights
})

results = results.sort_values(
    by="Weight",
    ascending=False
).reset_index(drop=True)

results.insert(
    0,
    "Rank",
    results.index + 1
)

results.to_csv(
    "ahp_requirement_weights.csv",
    index=False
)

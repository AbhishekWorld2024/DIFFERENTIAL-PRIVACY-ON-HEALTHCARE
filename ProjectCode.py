import numpy as np
import pandas as pd
import hashlib


def load_dataset(file_path):

    return pd.read_csv(file_path)


def add_laplace_noise(data, epsilon):

    if np.issubdtype(data.dtype, np.number):
        sensitivity = 1.0
        scale = sensitivity / epsilon
        noise = np.random.laplace(loc=0, scale=scale, size=len(data))
        return data + noise
    else:
        return data


def apply_data_masking(data, columns_to_mask, max_length=10):

    masked_data = data.copy()
    for column_to_mask in columns_to_mask:
        masked_data[column_to_mask] = '#' * min(max_length, len(data))
    return masked_data


def apply_tokenization(data, columns_to_tokenize):

    tokenized_data = data.copy()
    for column_to_tokenize in columns_to_tokenize:
        tokenized_data[column_to_tokenize + '_token'] = data[column_to_tokenize].apply(
            lambda x: hashlib.sha256(str(x).encode()).hexdigest())
    return tokenized_data


def apply_differential_privacy(df, columns_for_privacy, epsilon):

    for column_for_privacy in columns_for_privacy:
        df[column_for_privacy + '_with_privacy'] = add_laplace_noise(df[column_for_privacy], epsilon)
    return df


def display_and_save_dataset(df, csv_filename, columns_for_privacy):

    selected_columns = columns_for_privacy + ['Age_with_privacy', 'Billing Amount_with_privacy',
                                              'Room Number_with_privacy', 'Medical Condition_token', 'Hospital_token',
                                              'Insurance Provider_token', 'Medication_token']


    selected_columns = [col for col in selected_columns if col in df.columns]

    df_selected = df[selected_columns]


    columns_to_mask = ['Medical Condition', 'Name', 'Blood Type', 'Doctor']
    df_selected = apply_data_masking(df_selected, columns_to_mask, max_length=10)  # Set max_length as needed


    df_selected = df_selected.drop(columns=columns_for_privacy)

    print("\nHealthcare Dataset with Privacy Techniques:")
    print(df_selected.head())

    df_selected.to_csv(csv_filename, index=False)
    print(f"\nDataset with privacy saved to {csv_filename}")



excel_file_path = 'C:/Users/a772a265/Desktop/DataSet.csv'


healthcare_data = load_dataset(excel_file_path)


print("Original Healthcare Dataset (Numeric Columns Only):")
print(healthcare_data.select_dtypes(include='number').head())


epsilon = 0.5


columns_for_privacy = ['Age', 'Billing Amount', 'Room Number']


healthcare_data = apply_differential_privacy(healthcare_data, columns_for_privacy, epsilon)


columns_to_tokenize = ['Hospital', 'Insurance Provider', 'Medication']
healthcare_data = apply_tokenization(healthcare_data, columns_to_tokenize)


csv_filename = 'C:/Users/a772a265/Desktop/healthcare_dataset_with_privacy.csv'  # Add missing "/" and space
display_and_save_dataset(healthcare_data, csv_filename, columns_for_privacy)

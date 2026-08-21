import pandas as pd
import os

# Define the path to the CSV file
# csv_file_path    = 'C:\\Users\\vojtech.balint\\Downloads\\zoznam.csv'
# output_file_path = 'C:\\Users\\vojtech.balint\\Downloads\\zoznam_processed.csv'
csv_file_path    = 'preteky/2026-05-23_Zazriva/zoznam.csv'
output_file_path = csv_file_path.replace('.csv', '_processed.csv')

# Read the CSV file using pandas
def read_csv(file_path):
    try:
        df = pd.read_csv(file_path, delimiter=';')
        print(f"CSV file '{file_path}' read successfully.")
        print(df.info())
        print(df.head())
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def save_csv(df, output_path):
    try:
        # Save the DataFrame to a new CSV file with semicolon delimiter
        # and without the index column
        df.to_csv(output_path, index=False, sep=';')
        print(f"Processed data saved to '{output_path}' successfully.")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

# Function to reorder columns in the DataFrame
def reorder_columns(dataframe):
    new_order = [3, 2, 4, 1, 0, 5]
    return dataframe.iloc[:, new_order]

def convert_data(df):
    # Reorder the columns in the DataFrame
    # df = reorder_columns(df)
    # print("Columns reordered.")
    # print(df.info())
    # print(df.head())
    
    # Convert values in column 1 using the convert_category function
    df.iloc[:, 1] = df.iloc[:, 1].apply(convert_category)
    print("Categories converted.")
    print(df.info())
    print(df.head())

    return df

def convert_category(cat_in : str) -> str:
    # remove the dash from the category string
    cat = cat_in.replace('-', '')
    cat = cat.replace(' ', '')
    
    # if cat in ["M10", "W10", "MWR", "K", "N", "Open"]: # let thiese categories unchanged
    #     pass
    # elif cat.endswith(('A', 'B', 'E')): # If A or B is at the end of the string, do no change it
    #     pass
    # elif cat == "K3":
    #     cat = "K"
    # else:
    #     cat += "A" # Add A to the end of the string

    # kategorie pre MS SR
    # if cat in ["M12A", "W12A"]:
    #     pass
    # elif cat.endswith(('E')):
    #     pass
    # elif cat.endswith(('A')):
    #     cat = cat[:-1] + "E"  # Change A to E

    return cat

if __name__ == "__main__":
    df_vza = read_csv(csv_file_path)
    if df_vza is not None:
        df_isorienteering = convert_data(df_vza)
        save_csv(df_isorienteering, output_file_path)
        print("Processing completed.")
    else:
        print("Failed to read the CSV file.")

    # test_data = ["M21-A", "M21-B", "M21-", "M21", "W50-"]
    # for cat in test_data:
    #     print(f"Input: {cat} => Converted: {convert_category(cat)}")

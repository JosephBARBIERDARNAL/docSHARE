import os
import pandas as pd
import pyreadstat

def create_data():
   
   # initiate constants
   directory = 'data/'
   file_names = []
   waves = []
   columns = []
   labels = []

   # iterate through all files in the directory
   for root, dirs, files in os.walk(directory):
      for file in files:
         if file.endswith('.dta'):

               try:
                  dataset, meta = pyreadstat.read_dta(os.path.join(root, file))

                  column_names = list(meta.column_names)
                  column_labels = [label.replace(',', '') for label in meta.column_labels]
                  column_labels = list(meta.column_labels)

                  if len(column_names) != len(column_labels):
                     print(f'different number of column names and labels in {file}')
                     print(f'column names: {len(column_names)}')
                     print(f'column labels: {len(column_labels)}')

                  for col_name, label in zip(column_names, column_labels):
                     file_names.append(file)
                     waves.append(file[6])
                     columns.append(col_name)
                     labels.append(label)
                     print(label)
                  print(f"{file}")
                  print()
               
               except:
                  print('Error when opening:\n ', os.path.join(root, file))

               

   # create a dataframe with the results
   df = pd.DataFrame({
      'file_name': file_names,
      'wave': waves,
      'columns': columns,
      'labels': labels
   })
   df.to_csv('metadata-share.csv', index=False)

if __name__ == "__main__":
   create_data()
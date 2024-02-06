from setup.connector import get_database
import sys

file_path = sys.argv[1]

PATH_TO_FILE = sys.path[2]

collection = get_database(file_path)



file_name_list = os.listdir(PATH_TO_FILE)
end_value = min(567, len(file_name_list))
# Iterar sobre os intervalos de 10 em 10 até o valor 567 ou o número total de arquivos
for start_index in range(0, end_value, 10):
    end_index = min(start_index + 9, end_value - 1)
    lista = []
    
    for file_name in file_name_list[start_index:end_index + 1]:
        # Seu código atual aqui
        metadata = pd.read_csv(os.path.join(PATH_TO_FILE, file_name),
                               header=0,
                               nrows=8,
                               encoding='iso-8859-1',
                               sep=';',
                               decimal=',',
                               on_bad_lines='skip')

        df = pd.read_csv(os.path.join(PATH_TO_FILE, file_name),
                         header=8,
                         encoding='iso-8859-1',
                         sep=';',
                         decimal=',')

        rain_by_month = df[['Data', 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)']].groupby('Data')[
            'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].sum()

        lista.append({
            'nome_estacao': file_name[:-4],
            'UF': metadata.iloc[0, 1],
            'ESTACAO': metadata.iloc[1, 1],
            'CODIGO': metadata.iloc[2, 1],
            'LATITUDE': float(metadata.iloc[3, 1].replace(',', '.')),
            'LONGITUDE': float(metadata.iloc[4, 1].replace(',', '.')),
            'PLUVIO_ORIGEM': metadata.iloc[6, 1],
            'acumulado_dia': dict(zip(rain_by_month.index, rain_by_month))
        })
    collection.insert_many(lista)
        
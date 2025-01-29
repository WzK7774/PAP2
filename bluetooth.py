import serial
import mysql.connector

# Configurar a conexão Bluetooth (substituir COM3 pela porta correta)
porta_bluetooth = "COM3"  # No Linux pode ser "/dev/rfcomm0"
baud_rate = 9600

# Conectar ao Bluetooth
ser = serial.Serial(porta_bluetooth, baud_rate)
print("Conectado ao Bluetooth...")

# Conectar ao banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="usuario",
    password="senha",
    database="banco_de_dados"
)

cursor = db.cursor()

while True:
    try:
        # Lê os dados do Bluetooth
        dados = ser.readline().decode().strip()
        if dados:
            umidade = int(dados)  # Converter para número inteiro
            
            # Inserir no banco de dados
            sql = "INSERT INTO sensores (umidade, data_hora) VALUES (%s, NOW())"
            cursor.execute(sql, (umidade,))
            db.commit()

            print(f"Dado salvo: {umidade}%")
    except Exception as e:
        print("Erro:", e)
        break

# Fechar conexões
ser.close()
cursor.close()
db.close()

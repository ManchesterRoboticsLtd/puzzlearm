import time
from Arm_Lib import Arm_Device

# 1. Inicializar el objeto del brazo robótico
Arm = Arm_Device()
time.sleep(0.5)  # Breve pausa para asegurar la comunicación serial

print("=== Iniciando Ping de Servos en el Brazo Yahboom ===")

# El brazo DOFBOT tiene habitualmente 6 servos, mapeados del ID 1 al 6
# (El ID 6 suele ser la pinza y el ID 1 la base)
for servo_id in range(1, 7):
    posicion = Arm.Arm_serial_servo_read(servo_id)
        
    if posicion is not None:
        print(f"[OK] Servo ID {servo_id}: ¡Respuesta exitosa! Posición actual = {posicion}")
    else:
        print(f"[ERROR] Servo ID {servo_id}: No responde (Ping fallido).")
            
    time.sleep(0.1)  # Pequeña pausa entre lecturas para no saturar el bus

Arm.Arm_serial_servo_write(1,80,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(1,20,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(2,140,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(2,90,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(3,60,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(3,0,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(4,60,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(4,0,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(5,20,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(5,90,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(6,90,1000)
time.sleep(1)
Arm.Arm_serial_servo_write(6,180,1000)
time.sleep(1)

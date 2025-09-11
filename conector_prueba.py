try: 
    import mysql.connector
    print("✅ mysql.connector se importó correctamente.")
except ImportError as e:
    print("❌ No se pudo importar:", e) # valida el error

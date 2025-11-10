"""
Simulador de Máquina de Turing Determinista
Basado en la definición: M = (Q, Σ, Γ, δ, q0, qaccept, qreject)
"""

class TuringMachine:
    def __init__(self):
        self.Q = set()  # Conjunto de estados
        self.Sigma = set()  # Alfabeto de entrada
        self.Gamma = set()  # Alfabeto de la cinta
        self.delta = {}  # Función de transición
        self.q0 = None  # Estado inicial
        self.qaccept = None  # Estado de aceptación
        self.qreject = None  # Estado de rechazo
        self.blank = '⊔'  # Símbolo blanco
        
    def load_from_file(self, filename):
        """Carga la especificación de la máquina desde un archivo"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() 
                        if line.strip() and not line.strip().startswith('#')]
            
            # Parsear las secciones
            i = 0
            while i < len(lines):
                line = lines[i]
                
                if line.startswith('Q:'):
                    self.Q = set(line[2:].strip().split(','))
                elif line.startswith('Sigma:'):
                    self.Sigma = set(line[6:].strip().split(','))
                elif line.startswith('Gamma:'):
                    self.Gamma = set(line[6:].strip().split(','))
                elif line.startswith('q0:'):
                    self.q0 = line[3:].strip()
                elif line.startswith('qaccept:'):
                    self.qaccept = line[8:].strip()
                elif line.startswith('qreject:'):
                    self.qreject = line[8:].strip()
                elif line.startswith('delta:'):
                    # Leer las transiciones
                    i += 1
                    while i < len(lines):
                        # Detener si encontramos otra sección (línea que contiene ':' pero no es transición)
                        if ':' in lines[i] and '->' not in lines[i]:
                            break
                        trans = lines[i].strip()
                        if trans:
                            self.parse_transition(trans)
                        i += 1
                    continue
                elif line.startswith('input:'):
                    input_string = line[6:].strip()
                    return input_string
                
                i += 1
            
            return ""
            
        except FileNotFoundError:
            raise Exception(f"Archivo {filename} no encontrado")
        except Exception as e:
            raise Exception(f"Error al cargar el archivo: {str(e)}")
    
    def parse_transition(self, trans):
        """Parsea una transición en formato: (q,a)->(q',b,D)"""
        try:
            # Formato: (estado,símbolo)->(estado',símbolo',dirección)
            left, right = trans.split('->')
            left = left.strip().strip('()')
            right = right.strip().strip('()')
            
            state, symbol = [x.strip() for x in left.split(',')]
            new_state, new_symbol, direction = [x.strip() for x in right.split(',')]
            
            self.delta[(state, symbol)] = (new_state, new_symbol, direction)
        except:
            raise Exception(f"Error al parsear transición: {trans}")
    
    def verify_specification(self):
        """Verifica que la especificación de la máquina sea correcta"""
        errors = []
        
        # Verificar que los conjuntos no estén vacíos
        if not self.Q:
            errors.append("Conjunto de estados Q está vacío")
        if not self.Sigma:
            errors.append("Alfabeto de entrada Σ está vacío")
        if not self.Gamma:
            errors.append("Alfabeto de cinta Γ está vacío")
        
        # Verificar que el símbolo blanco esté en Gamma
        if self.blank not in self.Gamma:
            errors.append(f"Símbolo blanco {self.blank} no está en Γ")
        
        # Verificar que Sigma esté contenido en Gamma
        if not self.Sigma.issubset(self.Gamma):
            errors.append("Σ no es subconjunto de Γ")
        
        # Verificar que el símbolo blanco no esté en Sigma
        if self.blank in self.Sigma:
            errors.append("Símbolo blanco no puede estar en Σ")
        
        # Verificar estados especiales
        if self.q0 not in self.Q:
            errors.append(f"Estado inicial {self.q0} no está en Q")
        if self.qaccept not in self.Q:
            errors.append(f"Estado de aceptación {self.qaccept} no está en Q")
        if self.qreject not in self.Q:
            errors.append(f"Estado de rechazo {self.qreject} no está en Q")
        if self.qaccept == self.qreject:
            errors.append("Estado de aceptación y rechazo no pueden ser iguales")
        
        # Verificar función de transición
        for (state, symbol), (new_state, new_symbol, direction) in self.delta.items():
            if state not in self.Q:
                errors.append(f"Estado {state} en δ no está en Q")
            if symbol not in self.Gamma:
                errors.append(f"Símbolo {symbol} en δ no está en Γ")
            if new_state not in self.Q:
                errors.append(f"Estado {new_state} en δ no está en Q")
            if new_symbol not in self.Gamma:
                errors.append(f"Símbolo {new_symbol} en δ no está en Γ")
            if direction not in ['L', 'R']:
                errors.append(f"Dirección {direction} debe ser L o R")
        
        return errors
    
    def run(self, input_string, max_steps=10000, debug=False):
        """Ejecuta la máquina de Turing sobre la cadena de entrada"""
        # Inicializar la cinta
        if input_string:
            tape = list(input_string)
        else:
            tape = [self.blank]
        
        # Configuración inicial
        state = self.q0
        head = 0
        step = 0
        configurations = []
        
        # Agregar configuración inicial
        config = self.get_configuration(tape[:], state, head)
        configurations.append(config)
        
        # Ejecutar la máquina
        while state != self.qaccept and state != self.qreject and step < max_steps:
            # Extender la cinta si es necesario
            if head < 0:
                tape.insert(0, self.blank)
                head = 0
            if head >= len(tape):
                tape.append(self.blank)
            
            # Leer el símbolo actual
            current_symbol = tape[head]
            
            # Debug: mostrar primeros 20 pasos
            if debug and step < 20:
                print(f"Paso {step}: estado={state}, cabeza={head}, símbolo='{current_symbol}', cinta={''.join(tape)}")
            
            # Buscar transición
            if (state, current_symbol) not in self.delta:
                # No hay transición definida, rechazar
                state = self.qreject
                config = self.get_configuration(tape[:], state, head)
                configurations.append(config)
                break
            
            # Aplicar transición
            new_state, new_symbol, direction = self.delta[(state, current_symbol)]
            
            if debug and step < 20:
                print(f"  -> nuevo_estado={new_state}, escribe='{new_symbol}', dirección={direction}")
            
            # Escribir nuevo símbolo
            tape[head] = new_symbol
            
            # Mover cabeza
            if direction == 'R':
                head += 1
            elif direction == 'L':
                head -= 1
                if head < 0:
                    tape.insert(0, self.blank)
                    head = 0
            
            # Actualizar estado
            state = new_state
            step += 1
            
            # Guardar configuración (solo cada 100 pasos si hay muchos)
            if step < 100 or step % 100 == 0 or state in [self.qaccept, self.qreject]:
                config = self.get_configuration(tape[:], state, head)
                configurations.append(config)
        
        # Resultado
        if step >= max_steps:
            result = "CICLO INFINITO (límite de pasos alcanzado)"
        elif state == self.qaccept:
            result = "ACEPTADA"
        elif state == self.qreject:
            result = "RECHAZADA"
        else:
            result = "DESCONOCIDO"
        
        return configurations, result
    
    def get_configuration(self, tape, state, head):
        """Genera la configuración en notación uqv"""
        # Eliminar blancos innecesarios al final
        while len(tape) > 1 and tape[-1] == self.blank:
            tape.pop()
        
        # Asegurar al menos un símbolo
        if not tape:
            tape = [self.blank]
        
        # Construir configuración
        left_part = ''.join(tape[:head])
        right_part = ''.join(tape[head:])
        
        if not right_part:
            right_part = self.blank
        
        config = f"{left_part}{state}{right_part}"
        return config
    
    def save_output(self, filename, configurations, result):
        """Guarda las configuraciones en un archivo de salida"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("CONFIGURACIONES DE LA MÁQUINA DE TURING\n")
            f.write("=" * 50 + "\n\n")
            
            for i, config in enumerate(configurations):
                f.write(f"{config}\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write(f"RESULTADO: {result}\n")
            f.write(f"Número de pasos: {len(configurations) - 1}\n")


def main():
    """Función principal"""
    import sys
    
    if len(sys.argv) != 3:
        print("Uso: python turing_simulator.py <archivo_entrada> <archivo_salida>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Crear máquina
        tm = TuringMachine()
        
        # Cargar especificación
        print("Cargando máquina de Turing...")
        input_string = tm.load_from_file(input_file)
        
        # Verificar especificación
        print("Verificando especificación...")
        errors = tm.verify_specification()
        if errors:
            print("\nERRORES EN LA ESPECIFICACIÓN:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        
        print("✓ Especificación correcta")
        
        # Ejecutar máquina
        print(f"\nEjecutando máquina con entrada: '{input_string}'")
        configurations, result = tm.run(input_string)
        
        # Guardar salida
        tm.save_output(output_file, configurations, result)
        print(f"\n✓ Resultado: {result}")
        print(f"✓ Configuraciones guardadas en: {output_file}")
        print(f"✓ Total de pasos: {len(configurations) - 1}")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

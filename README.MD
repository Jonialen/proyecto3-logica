# 🎯 Simulador de Máquina de Turing Determinista

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

*Una implementación completa y educativa de una Máquina de Turing Determinista*

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [Ejemplos](#-ejemplos) • [Formato](#-formato-de-entrada)

</div>

---

## 📖 Descripción

Este proyecto implementa un **Simulador de Máquina de Turing Determinista** basado en la definición formal:

$$M = (Q, \Sigma, \Gamma, \delta, q_0, q_{accept}, q_{reject})$$

Donde:
- **Q**: Conjunto finito de estados
- **Σ**: Alfabeto de entrada
- **Γ**: Alfabeto de la cinta (Σ ⊆ Γ)
- **δ**: Función de transición Q × Γ → Q × Γ × {L, R}
- **q₀**: Estado inicial
- **q_accept**: Estado de aceptación
- **q_reject**: Estado de rechazo

## ✨ Características

✅ **Validación completa** de la especificación de la máquina  
✅ **Notación estándar** para configuraciones (uqv)  
✅ **Detección de ciclos infinitos** con límite configurable de pasos  
✅ **Salida detallada** de todas las configuraciones  
✅ **Modo debug** para visualizar la ejecución paso a paso  
✅ **Manejo de errores** robusto y mensajes informativos  
✅ **Ejemplos incluidos** (aceptación, rechazo, ciclo infinito)  

## 🚀 Instalación

### Requisitos
- Python 3.7 o superior

### Clonar el repositorio
```bash
git clone https://github.com/Jonialen/proyecto3-logica.git
cd proyecto3-logica
```

No se requieren dependencias adicionales. ¡El simulador está listo para usar! 🎉

## 💻 Uso

### Sintaxis básica
```bash
python turing_simulator.py <archivo_entrada> <archivo_salida>
```

### Parámetros
- `<archivo_entrada>`: Archivo con la especificación de la MT y la cadena de entrada
- `<archivo_salida>`: Archivo donde se guardarán las configuraciones y el resultado

### Ejemplo
```bash
python turing_simulator.py mt_accept.txt salida.txt
```

## 📝 Ejemplos

El proyecto incluye tres casos de prueba:

### 1️⃣ Caso de Aceptación
```bash
python turing_simulator.py mt_accept.txt salida.txt
```
Máquina que reconoce el lenguaje $L = \\{0^n 1^n \mid n \geq 1\\}$  
**Entrada:** `0011`  
**Resultado:** ✅ ACEPTADA

### 2️⃣ Caso de Rechazo
```bash
python turing_simulator.py mt_reject.txt salida.txt
```
Máquina que reconoce el mismo lenguaje  
**Entrada:** `000111` (desbalanceada)  
**Resultado:** ❌ RECHAZADA

### 3️⃣ Caso de Ciclo Infinito
```bash
python turing_simulator.py mt_loop.txt salida.txt
```
Máquina diseñada para entrar en ciclo  
**Resultado:** 🔄 CICLO INFINITO

## 📋 Formato de Entrada

El archivo de especificación debe seguir este formato:

```plaintext
# Comentarios comienzan con #

# Conjunto de estados (separados por comas)
Q: q0,q1,q2,qaccept,qreject

# Alfabeto de entrada
Sigma: 0,1

# Alfabeto de la cinta (incluye símbolo blanco ⊔)
Gamma: 0,1,x,⊔

# Estado inicial
q0: q0

# Estado de aceptación
qaccept: qaccept

# Estado de rechazo
qreject: qreject

# Función de transición
# Formato: (estado_actual,símbolo_leído)->(estado_nuevo,símbolo_escrito,dirección)
delta:
(q0,0)->(q1,x,R)
(q1,1)->(q2,x,L)
(q2,⊔)->(qaccept,⊔,R)

# Cadena de entrada
input: 01
```

### Reglas importantes:
- El símbolo blanco se representa como `⊔`
- Las direcciones son: `L` (izquierda) o `R` (derecha)
- Cada transición en una línea separada
- Los comentarios (`#`) son opcionales

## 📤 Formato de Salida

El archivo de salida contiene:

```plaintext
CONFIGURACIONES DE LA MÁQUINA DE TURING
==================================================

q00011
xq10011
x0q2011
...
xxxxq4⊔

==================================================
RESULTADO: ACEPTADA
Número de pasos: 15
```

Las configuraciones usan la **notación uqv**, donde:
- `u`: contenido de la cinta antes del cabezal
- `q`: estado actual
- `v`: contenido desde el cabezal hasta el final

## 🔍 Validaciones

El simulador verifica automáticamente:

- ✓ Conjuntos Q, Σ y Γ no vacíos
- ✓ Σ ⊆ Γ
- ✓ Símbolo blanco ∈ Γ pero ∉ Σ
- ✓ Estados q₀, qaccept, qreject ∈ Q
- ✓ qaccept ≠ qreject
- ✓ Todas las transiciones usan estados y símbolos válidos
- ✓ Direcciones solo pueden ser L o R

## 📊 Ejemplo de Ejecución

```
$ python turing_simulator.py mt_accept.txt salida.txt

Cargando máquina de Turing...
Verificando especificación...
✓ Especificación correcta

Ejecutando máquina con entrada: '0011'

✓ Resultado: ACEPTADA
✓ Configuraciones guardadas en: salida.txt
✓ Total de pasos: 15
```

## 🛠️ Estructura del Proyecto

```
proyecto3-logica/
│
├── turing_simulator.py    # Simulador principal
├── mt_accept.txt          # Ejemplo: caso de aceptación
├── mt_reject.txt          # Ejemplo: caso de rechazo
├── mt_loop.txt            # Ejemplo: ciclo infinito
├── salida.txt             # Archivo de salida generado
└── README.md              # Este archivo
```

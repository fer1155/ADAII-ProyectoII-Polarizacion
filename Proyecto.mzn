% modelo para minimizar la polarizacion (minpol)
% programacion entera mixta (las variables de movimiento x son enteras)

% *************************
% parametros quie recive el modelo
% *************************
int: n; % numero total de personas
int: m; % numero de posibles opiniones

array[1..m] of int: p; % distribucion inicial de personas por opinion (p)
array[1..m] of float: v; % valores reales asociados a las opiniones (v)
array[1..m, 1..3] of int: s; % matriz de personas con opinion inicial i y nivel de resistencia k (s)

float: ct; % costo total maximo permitido (ct)
float: maxMovs; % cantidad maxima de movimientos permitidos (maxmovs)

% costos unitarios por nivel de resistencia (1:baja, 2:media, 3:alta)
array[1..3] of float: res_cost = [1.0, 1.5, 2.0];

% *************************
% variables de decision
% *************************
% x[k, i, j]: personas con resistencia k que se mueven de opinion i a opinion j
array[1..3, 1..m, 1..m] of var int: x;

% p_prime[j]: distribucion final de personas con opinion j
array[1..m] of var 0..n: p_prime;

% med_pos: indice (1..m) de la opinion que sera la mediana
var 1..m: med_pos;

% med: el valor real de la mediana (v[med_pos])
var float: med = v[med_pos];

% polarizacion total final (funcion objetivo)
var float: total_polarization;


% *************************
% restricciones
% *************************

% x[k, i, i] = 0 (no se permite el movimiento a la misma opinion)
constraint forall(k in 1..3, i in 1..m) (
    x[k, i, i] = 0
);

% los movimientos deben ser no negativos
constraint forall(k in 1..3, i in 1..m, j in 1..m) (
    x[k, i, j] >= 0
);

% limite de personas por grupo inicial y resistencia
constraint forall(i in 1..m, k in 1..3) (
    sum(j in 1..m) (x[k, i, j]) <= s[i, k]
);

% calculo de la distribucion final (p_prime)
constraint forall(j in 1..m) (
    p_prime[j] = p[j] + 
                  sum(k in 1..3, i in 1..m) (x[k, i, j]) - % personas que llegan a j
                  sum(k in 1..3, l in 1..m) (x[k, j, l])    % personas que se van de j
);

% restriccion de costo total maximo (ct)
constraint 
    sum(k in 1..3, i in 1..m, j in 1..m) ( 
        abs(v[i] - v[j]) * res_cost[k] * int2float(x[k, i, j]) 
    ) <= ct;

% restriccion de movimientos maximos (|i-j|)
constraint
    sum(k in 1..3, i in 1..m, j in 1..m) ( 
        abs(i - j) * int2float(x[k, i, j]) 
    ) <= maxMovs;

% definicion de la mediana (med_pos)
% la mediana se define como el v[med_pos] si la poblacion a la izquierda 
% es menor a n/2 y la poblacion a la derecha es menor o igual a n/2
constraint sum(i in 1..(med_pos-1)) (p_prime[i]) < n / 2;
constraint sum(i in (med_pos+1)..m) (p_prime[i]) <= n / 2;


% calculo de la polarizacion total
constraint 
    total_polarization = sum(j in 1..m) ( int2float(p_prime[j]) * abs(v[j] - med) );


% *************************
% funcion objetivo
% *************************
solve minimize total_polarization;


% *************************
% salida del programa
% *************************

output [
    show(round(total_polarization * 1000.0)) ++ "\n", % polarizacion final
    "1\n", % nivel de resistencia baja (1)

    % matriz de movimientos para resistencia baja (k=1)
    % x[1, i, j] - personas que se mueven de i a j con resistencia 1
    show(x[1, 1, 1]) ++ "," ++ show(x[1, 1, 2]) ++ "," ++ show(x[1, 1, 3]) ++ "\n",
    show(x[1, 2, 1]) ++ "," ++ show(x[1, 2, 2]) ++ "," ++ show(x[1, 2, 3]) ++ "\n",
    show(x[1, 3, 1]) ++ "," ++ show(x[1, 3, 2]) ++ "," ++ show(x[1, 3, 3]) ++ "\n",
    
    % matriz de movimientos para resistencia media (k=2)
    "2\n", % nivel de resistencia media (2)
    show(x[2, 1, 1]) ++ "," ++ show(x[2, 1, 2]) ++ "," ++ show(x[2, 1, 3]) ++ "\n",
    show(x[2, 2, 1]) ++ "," ++ show(x[2, 2, 2]) ++ "," ++ show(x[2, 2, 3]) ++ "\n",
    show(x[2, 3, 1]) ++ "," ++ show(x[2, 3, 2]) ++ "," ++ show(x[2, 3, 3]) ++ "\n",

    % matriz de movimientos para resistencia alta (k=3)
    "3\n", % nivel de resistencia alta (3)
    show(x[3, 1, 1]) ++ "," ++ show(x[3, 1, 2]) ++ "," ++ show(x[3, 1, 3]) ++ "\n", 
    show(x[3, 2, 1]) ++ "," ++ show(x[3, 2, 2]) ++ "," ++ show(x[3, 2, 3]) ++ "\n", 
    show(x[3, 3, 1]) ++ "," ++ show(x[3, 3, 2]) ++ "," ++ show(x[3, 3, 3]) ++ "\n"
];
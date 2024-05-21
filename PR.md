Para criar a 'med_doencas.ttl', com a 'medical.ttl' como base:
- abrir o ficheiro 'Disease_Syntoms.csv' e separar a doença dos sintomas.
- adicionar a doença a uma lista para verificar que não há repetições.
- adicionar os sintomas a uma lista para verificar que não há repetições.
- abrir o ficheiro 'Disease_Description.csv' e separar a doença da descrição.
- adicionar a descrição a um dicionário do tipo {doença: descrição}
- escrever para o ficheiro de output os sintomas, com a estrutura estraida do ficheiro ttl derivado de 'medical.ttl'.
- escrever para o ficheiro de output as doenças, com a estrutura estraida do ficheiro ttl derivado de 'medical.ttl'.

Sempre que foi adicionado um elemento as listas ou ficheiro foram tratados os caractéres problemáticos((,),", ).

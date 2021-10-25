#include <max6675.h> //INCLUSÃO DE BIBLIOTECA
 
int thermofrioSO = 2;
int thermofrioCS = 3;
int thermofrioCLK = 4;
MAX6675 thermofrio(thermofrioCLK, thermofrioCS, thermofrioSO);

int thermomedioSO = 5; //PINO DIGITAL (SO)
int thermomedioCS = 6; //PINO DIGITAL (CS)
int thermomedioCLK = 7; //PINO DIGITAL (CLK / SCK)
MAX6675 thermomedio(thermomedioCLK, thermomedioCS, thermomedioSO); //CRIA UMA INSTÂNCIA UTILIZANDO OS PINOS (CLK, CS, SO)

int thermoquenteSO = 8;
int thermoquenteCS = 9;
int thermoquenteCLK = 10;
MAX6675 thermoquente(thermoquenteCLK, thermoquenteCS, thermoquenteSO);
  
void setup(){
  Serial.begin(9600); //INICIALIZA A SERIAL
  delay(1000); //INTERVALO
}
 
void loop(){
   // Serial.print("Temperatura: "); //IMPRIME O TEXTO NO MONITOR SERIAL
   Serial.print(thermofrio.readCelsius()); //IMPRIME NO MONITOR SERIAL A TEMPERATURA MEDIDA
   Serial.print("  ");
   // Serial.print(thermomedio.readCelsius());
   // Serial.print("  ");
   Serial.println(thermoquente.readCelsius());
   // Serial.println("*C"); //IMPRIME O TEXTO NO MONITOR SERIAL
   delay(2000); //INTERVALO
}

#include <LiquidCrystal.h>
#include <EEPROM.h>
// Sensores simulados
const int PINO_RIO = A0;
const int PINO_INTEGRIDADE = A1;

// Atuadores
const int LED_VERDE = 8;
const int LED_AMARELO = 9;
const int LED_VERMELHO = 10;
const int BUZZER = 11;

// LCD 16x2
const int LCD_RS = 12;
const int LCD_E = 7;
const int LCD_D4 = 5;
const int LCD_D5 = 4;
const int LCD_D6 = 3;
const int LCD_D7 = 2;

LiquidCrystal lcd(LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7);

// Controle de tempo sem delay()
unsigned long tempoAnteriorLeitura = 0;
unsigned long tempoAnteriorBuzzer = 0;

const unsigned long INTERVALO_LEITURA = 500;
const unsigned long INTERVALO_BUZZER = 300;

// Endereços da EEPROM para salvar contadores de erro
const int ENDERECO_ERROS_RIO = 0;
const int ENDERECO_ERROS_INTEGRIDADE = 4;

// Variáveis dos sensores
int nivelRio = 0;
int integridadeEstacao = 0;

// Contadores de erro
unsigned int contadorErrosRio = 0;
unsigned int contadorErrosIntegridade = 0;

// Status do sistema
String statusSistema = "NORMAL";

void setup() {
  Serial.begin(9600);

  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARELO, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  desligarAtuadores();

  lcd.begin(16, 2);
  lcd.clear();

  // Recupera contadores de erro salvos na EEPROM
  EEPROM.get(ENDERECO_ERROS_RIO, contadorErrosRio);
  EEPROM.get(ENDERECO_ERROS_INTEGRIDADE, contadorErrosIntegridade);

  // Proteção caso a EEPROM esteja com lixo de memória
  if (contadorErrosRio > 10000) {
    contadorErrosRio = 0;
    EEPROM.put(ENDERECO_ERROS_RIO, contadorErrosRio);
  }

  if (contadorErrosIntegridade > 10000) {
    contadorErrosIntegridade = 0;
    EEPROM.put(ENDERECO_ERROS_INTEGRIDADE, contadorErrosIntegridade);
  }

  lcd.setCursor(0, 0);
  lcd.print("Orbital Memory");
  lcd.setCursor(0, 1);
  lcd.print("Station Online");

  Serial.println("==========================================");
  Serial.println("ORBITAL MEMORY STATION");
  Serial.println("Sistema iniciado com millis(), sem delay().");
  Serial.println("Contadores recuperados da EEPROM.");
  Serial.println("==========================================");

  Serial.print("Erros Rio salvos: ");
  Serial.println(contadorErrosRio);

  Serial.print("Erros Integridade salvos: ");
  Serial.println(contadorErrosIntegridade);

  Serial.println("------------------------------------------");
}

void loop() {
  unsigned long tempoAtual = millis();

  if (tempoAtual - tempoAnteriorLeitura >= INTERVALO_LEITURA) {
    tempoAnteriorLeitura = tempoAtual;

    lerSensores();
    classificarStatus();
    atualizarAtuadores();
    atualizarDisplay();
    registrarTelemetria();
  }

  controlarBuzzer(tempoAtual);
}

// =====================================================
// Leitura e validação dos sensores
// =====================================================
void lerSensores() {
  int leituraRio = analogRead(PINO_RIO);
  int leituraIntegridade = analogRead(PINO_INTEGRIDADE);

  if (!leituraValida(leituraRio)) {
    contadorErrosRio++;
    EEPROM.put(ENDERECO_ERROS_RIO, contadorErrosRio);
    Serial.println("ERRO: leitura invalida no sensor do rio.");
    return;
  }

  if (!leituraValida(leituraIntegridade)) {
    contadorErrosIntegridade++;
    EEPROM.put(ENDERECO_ERROS_INTEGRIDADE, contadorErrosIntegridade);
    Serial.println("ERRO: leitura invalida no sensor de integridade.");
    return;
  }

  nivelRio = map(leituraRio, 0, 1023, 0, 100);
  integridadeEstacao = map(leituraIntegridade, 0, 1023, 0, 100);
}

bool leituraValida(int leitura) {
  return leitura >= 0 && leitura <= 1023;
}

// =====================================================
// Classificação automática do estado do sistema
// =====================================================
void classificarStatus() {
  if (nivelRio >= 80 || integridadeEstacao <= 40) {
    statusSistema = "CRITICO";
  } 
  else if (nivelRio >= 60 || integridadeEstacao <= 60) {
    statusSistema = "ATENCAO";
  } 
  else {
    statusSistema = "NORMAL";
  }
}

// =====================================================
// Atuação automática com LEDs
// =====================================================
void atualizarAtuadores() {
  if (statusSistema == "NORMAL") {
    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(LED_AMARELO, LOW);
    digitalWrite(LED_VERMELHO, LOW);
    noTone(BUZZER);
  }

  else if (statusSistema == "ATENCAO") {
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_AMARELO, HIGH);
    digitalWrite(LED_VERMELHO, LOW);
    noTone(BUZZER);
  }

  else if (statusSistema == "CRITICO") {
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_AMARELO, LOW);
    digitalWrite(LED_VERMELHO, HIGH);
  }
}

// =====================================================
// Buzzer com temporização não bloqueante
// =====================================================
void controlarBuzzer(unsigned long tempoAtual) {
  if (statusSistema == "CRITICO") {
    if (tempoAtual - tempoAnteriorBuzzer >= INTERVALO_BUZZER) {
      tempoAnteriorBuzzer = tempoAtual;
      tone(BUZZER, 750, 100);
    }
  } 
  else {
    noTone(BUZZER);
  }
}

// =====================================================
// Display LCD 16x2 com telemetria local
// =====================================================
void atualizarDisplay() {
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("R:");
  lcd.print(nivelRio);
  lcd.print("% ");

  lcd.print("E:");
  lcd.print(integridadeEstacao);
  lcd.print("%");

  lcd.setCursor(0, 1);
  lcd.print("Status:");
  lcd.print(statusSistema);
}

// =====================================================
// Registro da telemetria no Serial Monitor
// =====================================================
void registrarTelemetria() {
  Serial.print("Rio: ");
  Serial.print(nivelRio);
  Serial.print("% | Integridade: ");
  Serial.print(integridadeEstacao);
  Serial.print("% | Status: ");
  Serial.print(statusSistema);

  Serial.print(" | Erros Rio: ");
  Serial.print(contadorErrosRio);

  Serial.print(" | Erros Integridade: ");
  Serial.println(contadorErrosIntegridade);
}

// =====================================================
// Desliga todos os atuadores no início do sistema
// =====================================================
void desligarAtuadores() {
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_AMARELO, LOW);
  digitalWrite(LED_VERMELHO, LOW);
  digitalWrite(BUZZER, LOW);
  noTone(BUZZER);
}
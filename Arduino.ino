String str;
int dtr,st,rot,del;//dtr is direction pin and st is step pin, rot is for rotation, del for delay
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(2,OUTPUT);
  pinMode(8,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0)
  {str=Serial.readStringUntil('\n');
  int num=str.length();
  for(int i=0;i<num;i+=3)
  {
  char C=str[i];
  char D=str[i+1];
  char E=str[i+3];
    
    if (C=='R')
    {
     dtr=2;
     st=8;
  
  }
   if (C=='L')
    {
     dtr=3;
     st=9;
  
  }
   if (C=='U')
    {
     dtr=4;
     st=10;
  
  }
   if (C=='D')
    {
     dtr=5;
     st=11;
  
  }
   if (C=='F')
    {
     dtr=6;
     st=12;
  
  }
   if (C=='B')
    {
     dtr=7;
     st=13;
  
  }
   if(D=='2')
   {
    rot=1600;
   }
   if(D=='1'){
    rot=800;
   }
   if(D=='3')
   {
    for(int x=0;x<800;x++)
  {digitalWrite(dtr,HIGH);
    digitalWrite(st,HIGH);
    delayMicroseconds(100);
    digitalWrite(st,LOW);
    delayMicroseconds(100);}
  delay(50);}
    if(D=='1' || D=='2')
   {for(int x=0;x<rot;x++)
  {digitalWrite(dtr,LOW);
    digitalWrite(st,HIGH);
    delayMicroseconds(100);
    digitalWrite(st,LOW);
    delayMicroseconds(100);}
  delay(50);}
  }}
  
  }

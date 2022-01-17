// Patterns of Heat
// Gaëtan Robillard

import java.io.File.*;
import java.util.Date;

int milliseconds = 0;
int seconds = 0;
boolean start = true;
boolean zero;

int margin = 140;
int rows = 41;
int cols = 22;
int u; // the width of a unit
int count;

float xoff = 0.0;
int coef = 0;
int nTweets = 896;
int tmax = 65;
boolean dir;
float[] temp;

int tempMax = -33;
int tempMin = 66;
color fHue = tempMin;
color from;
color to;

PImage img;

JSONArray values;
String jsonFile = "../claim_monitor/collection.json"; //to delete
String path = "../claim_monitor/collections";
String field = "text";
String theTweet;
String oldest;
String[] categories = new String[nTweets];

String[] page = new String[8];
int wordMax = 8;
int cursor = 0;
int jump = 0;

PFont font;

boolean rotate = true;

void setup() {
  fullScreen();
  noCursor();
  // size(1920, 1080);
  // size(1080,1920);
  // size(608, 1080);

  background(255);
  frameRate(6);
  colorMode(HSB,100);
  img = loadImage("labels03.jpg");

  if (rotate){
    font = loadFont("FuturaLT-Book-32.vlw");
    textFont(font, 18);
    rotate(radians(-90));
    translate(-height, 0);
    u = (height - margin*2) / cols; // defines cell's dimension
  }
  else {
    font = loadFont("FuturaLT-Book-12.vlw");
    textFont(font, 12);
    u = (width - (margin*2)) / cols;
  }
  
  temp(); // array of temperatures
  display();
  jsonRead();
  jsonDisplay(theTweet);
}

void draw() {
  rectMode(CORNER);
  int cycle = 340;
  chrono(start);
  if (rotate){
    rotate(radians(-90));
    translate(-height, 0);
  }
  if (frameCount % cycle == 0){
    bg();
    temp();
    display();
    chrono(zero);
    jsonRead();
    jsonDisplay(theTweet);
    println("CYCLE");
    saveFrame("viz_####.jpg");
  }
  if (seconds == 15){
    bg();
    labels();
    filter(INVERT);
  }
  if (seconds == 15 && milliseconds > 1){
    bg();
    labels();
  }
}

void chrono(boolean trigger){
  if(trigger){
    if(int(millis()/100)  % 10 != milliseconds){
      milliseconds++;
    }
  }
  if (milliseconds >= 10){
    milliseconds -= 10;
    seconds++;
    println(seconds + "." + milliseconds);
  }
  if(trigger == false){
    milliseconds = 0;
    seconds = 0;
  }
}

void jsonRead(){
  compare();
  values = loadJSONArray(path + "/" + oldest);
  JSONObject tweet = values.getJSONObject(0);
  if (tweet != null){
    theTweet = tweet.getString(field);
  }
  else {
    print("new JSONObject couldn't be created");
  }
}

void dataRead(String data){
  compare();
  values = loadJSONArray(path + "/" + oldest);
  println("Json total documents: ", values.size());
  for (int i = 0 ; i < values.size() ; i++){
    JSONObject tweet = values.getJSONObject(i);
    categories[i] = tweet.getString(data);
  }
}

void compare(){
  File[] files = listFiles(path);
  int sum = (int)(files[1].lastModified()-files[0].lastModified());
  if (sum > 0){
    oldest = "collection-1.json";
    println("collection-1");
  }
  else {
    oldest = "collection-2.json";
    println("collection-2");
  }
  println("-----------------------");
}

void jsonDisplay(String t){
  jump = 0;
  fill(0,0,0);
  carriage(t); // fills page
  if(rotate){
    translate(0,height-margin-140);
  }
  for (int i = 0;   i< page.length; i++){
    text(page[i],margin,height-margin-60+jump);
    jump += 18;
  }
}

void carriage(String t){
  cursor = 0;
  String[] words = splitTokens(t);
  for (int i = 0; i< page.length; i++){
    page[i]="";
  }
  for (int i = 0; i< words.length; i++){
    if (i != 0 && i % wordMax == 0){
      page[cursor] = page[cursor] + words[i] + " ";
      cursor ++;
    }
    else {
      page[cursor] = page[cursor] + words[i] + " ";
    }
  }
}

void bg(){
    noStroke();
    fill(100,0,100);
    rect(0,0,height,width);
}

void labels(){
  //float w = (width-margin*2)*1.2;
  //float h = 16*w/9;
  image(img, 0, 0, height, width);
}

void display(){
  float value;
  dataRead("category"); // outputs array categories
  count = 0;
  noStroke();
  fill(fHue,100,50);
  rect(margin,margin,u*cols,u*rows-u);
  for (int i = 0; i<rows; i++) {
    for (int j = 0; j<cols; j++) {
      count++;
      int x = margin+j*u;
      int y = margin+i*u;
      if (categories[count-1].equals("0_0") == true){
        fHue = tempMin;
        value = map(temp[count-1],0,nTweets/2,tempMin,tempMax+30);
      }
      else {
        fHue = tempMin - 10;
        value = map(temp[count-1],0,nTweets/2,tempMin,tempMax);
      }
      if (i%2==0){
        heatMap(x+u, y+u/2, fHue, value, 6);
      }
      else {
        heatMap(x+u/2, y+u/2, fHue, value, 6);
      }
      if (count == nTweets) {
        break;
      } 
    }
  }
}

void heatMap(int xpos, int ypos, float f, float t, float def){
  rectMode(CENTER);
  int from = color(f, 100, 50);
  int to = color(t, 100, 100);
  for (int i = 0; i <= def; i++) {
    float w0 = lerp(u, u-10, i/def);
    float c = lerp(2, u/2, i/def);
    color gradient = lerpColor(from, to, i/def);
    fill(gradient);
    rect(xpos, ypos, w0, w0, c);
  }
}

void temp(){
  temp = new float[cols*rows];
  coef = 0;
  for (int i = 0; i < nTweets; i++){
    xoff = xoff + .01;
    if (coef > nTweets / 2) {
      dir = !dir;
    }
    if (dir == true) {
      coef+=-1;
    }
    if (coef < 0 && dir == true) {
      dir = !dir;
    } else if (!dir) {
      coef+=1;
    }
    temp[i]=noise(xoff)*coef;
  }
}

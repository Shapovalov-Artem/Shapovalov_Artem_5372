#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
using namespace std;

struct Student {
  string fio;
  char sex;
  int group_number;
  int number;
  int grades[8];
};

double Average(Student student){
  double average = 0;
  for(int i = 0; i < 8; i++) {
      average += student.grades[i];
  }
  return average /= 8;
}

int CheckScholarship(Student student){
  int flag = 0;
  for(int i = 0; i < 8; i++){
    if(student.grades[i]<4){
      flag = 1;
    }
  }
  return flag;
}

int CheckOnlyFive(Student student){
  int flag = 1;
  for(int i = 0; i < 8; i++){
    if(student.grades[i]!=5){
      flag = 0;
    }
  }
  return flag;
}

int CheckNoThree(Student student){
  int flag = 1;
  for(int i = 0; i < 8; i++){
    if(student.grades[i]<4){
      flag = 0;
    }
  }
  return flag;
}

int LoadStudents(Student students[], string &filename, int size) {
    ifstream file(filename);
    if (!file.is_open()) {
        return 0;
    }
    
    int cnt = 0;
    string line;
    
    while (getline(file, line) && cnt < size) {
        stringstream ss(line);
        string token;
        
        getline(ss, students[cnt].fio, ',');
        
        getline(ss, token, ',');
        students[cnt].sex = token[0];
        
        getline(ss, token, ',');
        students[cnt].group_number = stoi(token);
        
        getline(ss, token, ',');
        students[cnt].number = stoi(token);
        
        for (int i = 0; i < 8; i++) {
            getline(ss, token, ',');
            students[cnt].grades[i] = stoi(token);
        }
        
        cnt++;
    }
    
    file.close();
    return cnt;
}

void WriteNewStudent(Student students[], int &cnt, string &filename){
  Student student;
  bool validinput = false;

  cout << "Введите ФИО: ";
  cin.ignore(1000, '\n');
  getline(cin, student.fio);

  validinput = false;
  while(!validinput){
    cout << "Введите пол(m/f):";
    if(!(cin >> student.sex) || (student.sex!='m' && student.sex!='f')){
      cout << "Invalid input" << endl;
      cin.clear();
      cin.ignore(1000, '\n');
    } else{
      validinput = true;
    }
  }

  validinput = false;
  while(!validinput){
    cout << "Введите номер группы:";
    if(!(cin >> student.group_number) || student.group_number < 1000 || student.group_number > 9999){
      cout << "Invalid input" << endl;
      cin.clear();
      cin.ignore(1000, '\n');
  } else{
    validinput = true;
  }
  }
  
  validinput = false;
  while(!validinput){
    cout <<"Введите номер в группе: ";
    if(!(cin >> student.number) || student.number < 1){
      cout << "Invalid input" << endl;
      cin.clear();
      cin.ignore(1000, '\n');
    } else{
      validinput = true;
    }
  }

  validinput = false;
  cout << "Введите 8 оценок: ";
  while (!validinput) {
    bool hasBadGrade = false;
    
    for(int i = 0; i < 8; i++) {
      cin >> student.grades[i];
      
      if (cin.fail()) {
        cout << "Invalid input" << endl;
        cin.clear();
        cin.ignore(1000, '\n');
        hasBadGrade = true;
        break;
      }
      
      if (student.grades[i] < 2 || student.grades[i] > 5) {
        cout << "Invalid input" << endl;
        hasBadGrade = true;
        break;
      }
      
      if (student.grades[i] == 2) {
        cout << "Ошибка: студент имеет двойку и должен быть отчислен. Невозможно добавить." << endl;
        hasBadGrade = true;
        break;
      }
    }
    
    if (hasBadGrade) {
      cin.clear();
      cin.ignore(1000, '\n');
      cout << "Нажмите enter и повторите ввод всех 8 оценок: " << endl;
    } else {
      validinput = true;
    }
  }

  students[cnt] = student;

  ofstream file(filename, ios::app);
  file << student.fio << ','
       << student.sex << ','
       << student.group_number << ','
       << student.number << ',';
  for ( int i = 0; i < 8; i++){
    file << student.grades[i];
    if(i<7) file << ',';
  }
  file << endl;
  file.close();
  cnt++;
  cout << "Студент добавлен" << endl;
}

void PrintAllStudents(Student students[], int &cnt){
  if(cnt == 0){
    cout << "Список пуст!" << endl;
  } else{
     for(int i = 0; i < cnt; i++) {
              cout << i+1 << ". " << students[i].fio 
                    << " (гр." << students[i].group_number 
                    << ", пол: " << students[i].sex << ", номер в группе: " << students[i].number << ")" << endl;
              cout << "   Оценки: ";
              for(int j = 0; j < 8; j++) {
                  cout << students[i].grades[j] << " ";
              }
              cout << endl;
    }
  }
}

void PrintStudentOfNGroup(int N,Student students[], int &cnt){
  int flag = 0;
  for(int i = 0; i < cnt; i++) {
    if(students[i].group_number==N){
      cout << i+1 << ". " << students[i].fio 
                    << " (гр." << students[i].group_number 
                    << ", пол: " << students[i].sex << ", номер в группе: " << students[i].number << ")" << endl;
              cout << "   Оценки: ";
              for(int j = 0; j < 8; j++) {
                  cout << students[i].grades[j] << " ";
              }
              cout << endl;
      flag = 1;
    }
  }
  if(!flag) cout << "Нет данной группы" << endl;
}

void PrintStudentsOfKNumber(int K, Student students[],int &cnt){
   int flag = 0;
  for(int i = 0; i < cnt; i++) {
    if(students[i].number==K){
      cout << i+1 << ". " << students[i].fio 
                    << " (гр." << students[i].group_number 
                    << ", пол: " << students[i].sex << ", номер в группе: " << students[i].number << ")" << endl;
              cout << "   Оценки: ";
              for(int j = 0; j < 8; j++) {
                  cout << students[i].grades[j] << " ";
              }
              cout << endl;
      flag = 1;
    }
  }
  if(!flag) cout << "Нет студентов под номером " << K << endl;
}

void CountOfSexes(Student students[],int &cnt){
  int cnt_m = 0;
  int cnt_f = 0;
  for(int i = 0; i < cnt; i++) {
    if(students[i].sex=='m'){
      cnt_m++;
    } else cnt_f++;
  }
  cout << "Количество мальчиков: " << cnt_m << endl;
  cout << "Количество девочек: " << cnt_f << endl;
}

void PrintTopStudents(Student students[], int &cnt){
  if(cnt == 0){
    cout << "Список пуст!" << endl;
    return;
  }
  
  int indices[100];
  double averages[100];
  
  for(int i = 0; i < cnt; i++){
    indices[i] = i;
    averages[i] = Average(students[i]);
  }
  
  // сортировка пузырьком
  for(int i = 0; i < cnt - 1; i++){
    for(int j = 0; j < cnt - i - 1; j++){
      if(averages[j] < averages[j + 1]){
        swap(averages[j], averages[j + 1]);
        swap(indices[j], indices[j + 1]);
      }
    }
  }
  
  int topCount = (cnt < 3) ? cnt : 3;
  
  for(int i = 0; i < topCount; i++){
    int studentIndex = indices[i];
    cout << i+1 << ". " << students[studentIndex].fio 
         << " (гр." << students[studentIndex].group_number << ")" << endl;
    cout << "   Средний балл: " << averages[i] << endl;
    cout << "   Оценки: ";
    for(int j = 0; j < 8; j++) {
      cout << students[studentIndex].grades[j] << " ";
    }
    cout << "\n" << endl;
  }
}

void PrintStudentsWithoutScholarship(Student students[],int &cnt){
  cout << "Студенты без стипендии" << endl;
  for(int i = 0; i < cnt; i++) {
    if(CheckScholarship(students[i]) == 1){
      cout << i+1 << ". " << students[i].fio 
                    << " (гр." << students[i].group_number 
                    << ", пол: " << students[i].sex << ", номер в группе: " << students[i].number << ")" << endl;
              cout << "   Оценки: ";
              for(int j = 0; j < 8; j++) {
                  cout << students[i].grades[j] << " ";
              }
              cout << endl;
    }
  }
}

void PrintStudentsOnlyFive(Student students[],int &cnt){
  cout << "Студенты с одними пятерками" << endl;
  for(int i = 0; i < cnt; i++) {
    if(CheckOnlyFive(students[i]) == 1){
      cout << i+1 << ". " << students[i].fio 
                    << " (гр." << students[i].group_number 
                    << ", пол: " << students[i].sex << ", номер в группе: " << students[i].number << ")" << endl;
              cout << "   Оценки: ";
              for(int j = 0; j < 8; j++) {
                  cout << students[i].grades[j] << " ";
              }
              cout << endl;
    }
  }
}

void PrintStudentsWithoutThree(Student students[],int &cnt){
  cout << "Студенты без троек" << endl;
  for(int i = 0; i < cnt; i++) {
    if(CheckNoThree(students[i]) == 1){
      cout << i+1 << ". " << students[i].fio 
                    << " (гр." << students[i].group_number 
                    << ", пол: " << students[i].sex << ", номер в группе: " << students[i].number << ")" << endl;
              cout << "   Оценки: ";
              for(int j = 0; j < 8; j++) {
                  cout << students[i].grades[j] << " ";
              }
              cout << endl;
    }
  }
}

bool IsNumberUniqueInGroup(const Student students[], int cnt, int group_number, int student_number, int excludeIndex = -1) {
    for (int i = 0; i < cnt; i++) {
        if (i == excludeIndex) continue;
        
        if (students[i].group_number == group_number && students[i].number == student_number) {
            return false;
        }
    }
    return true;
}

void EditStudent(Student students[], int &cnt, string &filename){
  if(cnt == 0){
    cout << "Список пуст!" << endl;
    return;
  }
  
  int index;
  cin >> index;
  
  if(index < 1 || index > cnt || cin.fail()){
    cout << "Нет студента с таким id" << endl;
    cin.clear();
    cin.ignore(1000, '\n');
    return;
  }
  
  index--;
  
  string input;
  
  cout << "ФИО (" << students[index].fio << "): ";
  cin.ignore(1000, '\n');
  getline(cin, input);
  if(!input.empty()) students[index].fio = input;
  
  cout << "Пол (" << students[index].sex << "): ";
  getline(cin, input);
  if(!input.empty()) students[index].sex = input[0];
  
  cout << "Номер группы (" << students[index].group_number << "): ";
  getline(cin, input);
  if(!input.empty()) students[index].group_number = stoi(input);

  bool valid = false;
  while(!valid){
    cout << "Номер в группе (" << students[index].number << "): ";
    getline(cin, input);
    
    if(input.empty()) {
      valid = true;
    } else {
      int newNumber = stoi(input);
      if (IsNumberUniqueInGroup(students, cnt, students[index].group_number, newNumber, index)) {
        students[index].number = newNumber;
        valid = true;
      } else {
        cout << "Ошибка: студент с номером " << newNumber 
             << " уже существует в группе " << students[index].group_number << endl;
        cout << "Попробуйте снова или оставьте пустым для сохранения текущего номера" << endl;
        cin.clear();
        cin.ignore(1000,'\n');
      }
    }
  }
  
  
  cout << "Оценки (текущие: ";
  for(int i = 0; i < 8; i++) cout << students[index].grades[i] << " ";
  cout << "): " << endl;
  
  for(int i = 0; i < 8; i++){
    cout << "Оценка " << i+1 << ": ";
    getline(cin, input);
    if(!input.empty()) students[index].grades[i] = stoi(input);
  }
  
  ofstream file(filename);
  for(int i = 0; i < cnt; i++){
    file << students[i].fio << ','
         << students[i].sex << ','
         << students[i].group_number << ','
         << students[i].number << ',';
    for(int j = 0; j < 8; j++){
      file << students[i].grades[j];
      if(j < 7) file << ',';
    }
    file << endl;
  }
  file.close();
}


int main(){
  const int size = 100;
  struct Student students[size];
  string filename = "database.txt";
  int count_of_students = LoadStudents(students, filename, size);
  int choice = 0;

  while(choice!=11){
    cout << "Доступные операции:" << endl;
    cout << " 1. Добавить нового студента" << endl;
    cout << " 2. Показать всех студентов" << endl;
    cout << " 3. Найти студентов по номеру группы" << endl;
    cout << " 4. Найти студентов по номеру в группе" << endl;
    cout << " 5. Подсчитать количество мальчиков и девочек" << endl;
    cout << " 6. Показать топ-3 студентов по успеваемости" << endl;
    cout << " 7. Показать студентов-отличников (только 5)" << endl;
    cout << " 8. Показать студентов без стипендии (есть 3)" << endl;
    cout << " 9. Показать студентов без троек (4 и 5)" << endl;
    cout << "10. Редактировать данные студента" << endl;
    cout << "11. Выйти из программы" << endl;
    cin >> choice;
    switch(choice){
    case 1:
      if (count_of_students < size){
        WriteNewStudent(students, count_of_students, filename);
      } else{
        cout << "You have riched the limit of students" << endl;
      }
      break;
    case 2:
      PrintAllStudents(students,count_of_students);
      break;
    case 3:{
      int N;
      bool valid = false;
      while(!valid){
        if(!(cin >> N)){
          cout << "Invalid input" << endl;
          cin.clear();
          cin.ignore(1000, '\n');
        } else{
          valid = true;
        }
      }
      PrintStudentOfNGroup(N,students,count_of_students);
      break;
    }
    case 4:{
      int K;
      bool valid = false;
      while(!valid){
        if(!(cin >> K)){
          cout << "Invalid input" << endl;
          cin.clear();
          cin.ignore(1000, '\n');
        } else{
          valid = true;
        }
      }
      PrintStudentsOfKNumber(K,students,count_of_students);
      break;
      }
    case 5:
      CountOfSexes(students,count_of_students);
      break;
    case 6:
      PrintTopStudents(students,count_of_students);
      break;
    case 7:
      PrintStudentsOnlyFive(students,count_of_students);
      break;
    case 8:
      PrintStudentsWithoutScholarship(students,count_of_students);
      break;
    case 9:
      PrintStudentsWithoutThree(students,count_of_students);
      break;
    case 10:
      EditStudent(students, count_of_students, filename);
      break;
    case 11:
      break;
    }
  }
  return 0;
}
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
using namespace std;

struct Volunteer {
  string fio;
  int age;
  string role;
  int hours;
  int mmr;
  string number;
};

int LoadVolunteers(Volunteer volunteers[], string &filename, int size) {
    ifstream file(filename);
    if (!file.is_open()) {
        cout << "Не удалось открыть файл " << filename << endl;
        return 0;
    }
    
    int cnt = 0;
    string line;
    
    while (getline(file, line) && cnt < size) {
        stringstream ss(line);
        string token;
        
        getline(ss, volunteers[cnt].fio, ',');
        
        getline(ss, token, ',');
        volunteers[cnt].age = stoi(token);
        
        getline(ss, volunteers[cnt].role, ',');
        
        getline(ss, token, ',');
        volunteers[cnt].hours = stoi(token);
        
        getline(ss, token, ',');
        volunteers[cnt].mmr = stoi(token);
        
        getline(ss, volunteers[cnt].number, ',');
        
        cnt++;
    }
    
    file.close();
    return cnt;
}

void WriteNewVolunteer(Volunteer volunteers[], int &cnt, string &filename){
  Volunteer volunteer;
  cout << "Введите ФИО: ";
  cin.ignore();
  getline(cin, volunteer.fio);
  cout << "Введите возраст:";
  cin >> volunteer.age;
  cout << "Введите направление деятельности: ";
  cin.ignore();
  getline(cin, volunteer.role);
  cout << "Введите количество часов:";
  cin >> volunteer.hours;
  cout <<"Введите рейтинг: ";
  cin >> volunteer.mmr;
  cout << "Введите номер телефона: ";
  cin >> volunteer.number;

  volunteers[cnt] = volunteer;

  ofstream file(filename, ios::app);
  file << volunteer.fio << ','
       << volunteer.age << ','
       << volunteer.role << ','
       << volunteer.hours << ','
       << volunteer.mmr << ',' 
       << volunteer.number;
  file << endl;
  file.close();
  cnt++;
  cout << "Волонтер добавлен" << endl;
}

void PrintActiveVolunteers(Volunteer volunteers[], int &cnt, int N){
    for(int i = 0;i < cnt; i++){
        if(volunteers[i].hours>N){
            cout << i+1 << ". " << volunteers[i].fio << endl;
            cout << "   Возраст: " << volunteers[i].age << " лет" << endl;
            cout << "   Роль: " << volunteers[i].role << endl;
            cout << "   Отработано часов: " << volunteers[i].hours << endl;
            cout << "   Рейтинг (MMR): " << volunteers[i].mmr << endl;
            cout << "   Телефон: " << volunteers[i].number << endl;
        }
    }
}

void PrintVolunteersOfRole(Volunteer volunteers[], int &cnt, string Role){
    for(int i =0; i < cnt; i++){
        if(volunteers[i].role == Role){
            cout << i+1 << ". " << volunteers[i].fio << endl;
            cout << "   Возраст: " << volunteers[i].age << " лет" << endl;
            cout << "   Роль: " << volunteers[i].role << endl;
            cout << "   Отработано часов: " << volunteers[i].hours << endl;
            cout << "   Рейтинг (MMR): " << volunteers[i].mmr << endl;
            cout << "   Телефон: " << volunteers[i].number << endl;
        }
    }
}

void PrintEmergencyContacts(Volunteer volunteers[], int &cnt){
  if(cnt == 0){
    cout << "Список волонтеров пуст!" << endl;
    return;
  }
  
  int minHours;
  cout << "Введите минимальное количество часов для срочного вызова: ";
  cin >> minHours;
  
  bool found = false;
  for(int i = 0; i < cnt; i++) {
    if(volunteers[i].hours > minHours){
      cout << volunteers[i].fio << " - " << volunteers[i].number;
      cout << " (часов: " << volunteers[i].hours << ", рейтинг: " << volunteers[i].mmr << ")" << endl;
      found = true;
    }
  }
  
  if(!found){
    cout << "Нет волонтеров с опытом > " << minHours << " часов" << endl;
  }
}

int main(){
    const int size = 100;
    struct Volunteer volunteers[size];
    string filename = "base.txt";
    int count_of_volunteers = LoadVolunteers(volunteers, filename, size);
    int choice;

    while(choice!=5){
        cin >> choice;
        switch (choice){
        case 1:
            WriteNewVolunteer(volunteers,count_of_volunteers,filename);
            break;
        case 2:
            int N;
            cin >> N;
            PrintActiveVolunteers(volunteers,count_of_volunteers,N);
            break;
        case 3: {
            string Role;
            cin >> Role;
            PrintVolunteersOfRole(volunteers,count_of_volunteers,Role);
            break;
        }
        case 4:
            PrintEmergencyContacts(volunteers,count_of_volunteers);
            break;
        case 5:
            break;
        }
    }
}
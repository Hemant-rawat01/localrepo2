#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Student {
    int id;
    char name[50];
    char email[50];
    char contact[15];
    char address[100];
    char dob[15];
    char course[30];
    char branch[30];
    int semester;
    int year;
};

void addStudents() {
    struct Student s;
    FILE *fp = fopen("students.dat", "ab");
    int n, i;

    printf("Enter the number of students to add: ");
    scanf("%d", &n);

    for (i = 0; i < n; i++) {
        printf("\nAdding record for student %d:\n", i + 1);

        printf("Enter Student ID: ");
        scanf("%d", &s.id);
        getchar();
        printf("Enter Name: ");
        fgets(s.name, sizeof(s.name), stdin);
        s.name[strcspn(s.name, "\n")] = '\0';
        printf("Enter Email: ");
        fgets(s.email, sizeof(s.email), stdin);
        s.email[strcspn(s.email, "\n")] = '\0';
        printf("Enter Contact: ");
        fgets(s.contact, sizeof(s.contact), stdin);
        s.contact[strcspn(s.contact, "\n")] = '\0';
        printf("Enter Address: ");
        fgets(s.address, sizeof(s.address), stdin);
        s.address[strcspn(s.address, "\n")] = '\0';
        printf("Enter Date of Birth (DD/MM/YYYY): ");
        fgets(s.dob, sizeof(s.dob), stdin);
        s.dob[strcspn(s.dob, "\n")] = '\0';
        printf("Enter Course: ");
        fgets(s.course, sizeof(s.course), stdin);
        s.course[strcspn(s.course, "\n")] = '\0';
        printf("Enter Branch: ");
        fgets(s.branch, sizeof(s.branch), stdin);
        s.branch[strcspn(s.branch, "\n")] = '\0';
        printf("Enter Semester: ");
        scanf("%d", &s.semester);
        printf("Enter Year: ");
        scanf("%d", &s.year);

        fwrite(&s, sizeof(s), 1, fp);
    }

    fclose(fp);

    printf("\nStudent records added successfully!\n");
}

void displayStudents() {
    struct Student s;
    FILE *fp = fopen("students.dat", "rb");
    int count = 0;

    if (fp == NULL) {
        printf("No records found.\n");
        return;
    }

    printf("\n--- Student Records Report ---\n");
    printf("----------------------------------------------------------------------------------------------\n");
    printf("ID | Name                 | Email                 | Contact     | Course     | Branch     | Sem | Year\n");
    printf("----------------------------------------------------------------------------------------------\n");

    while (fread(&s, sizeof(s), 1, fp)) {
        printf("%2d | %-20s | %-20s | %-11s | %-10s | %-10s | %3d | %4d\n",
            s.id, s.name, s.email, s.contact, s.course, s.branch, s.semester, s.year);
        count++;
    }

    printf("----------------------------------------------------------------------------------------------\n");
    printf("Total Students: %d\n", count);

    fclose(fp);
}

void updateStudent() {
    struct Student s;
    FILE *fp = fopen("students.dat", "rb+");
    int id, found = 0;

    if (fp == NULL) {
        printf("No records found.\n");
        return;
    }

    printf("Enter Student ID to update: ");
    scanf("%d", &id);

    while (fread(&s, sizeof(s), 1, fp)) {
        if (s.id == id) {
            found = 1;
            fseek(fp, -sizeof(s), SEEK_CUR);

            printf("Enter New Name: ");
            getchar();
            fgets(s.name, sizeof(s.name), stdin);
            s.name[strcspn(s.name, "\n")] = '\0';
            printf("Enter New Email: ");
            fgets(s.email, sizeof(s.email), stdin);
            s.email[strcspn(s.email, "\n")] = '\0';
            printf("Enter New Contact: ");
            fgets(s.contact, sizeof(s.contact), stdin);
            s.contact[strcspn(s.contact, "\n")] = '\0';
            printf("Enter New Address: ");
            fgets(s.address, sizeof(s.address), stdin);
            s.address[strcspn(s.address, "\n")] = '\0';
            printf("Enter New DOB: ");
            fgets(s.dob, sizeof(s.dob), stdin);
            s.dob[strcspn(s.dob, "\n")] = '\0';
            printf("Enter New Course: ");
            fgets(s.course, sizeof(s.course), stdin);
            s.course[strcspn(s.course, "\n")] = '\0';
            printf("Enter New Branch: ");
            fgets(s.branch, sizeof(s.branch), stdin);
            s.branch[strcspn(s.branch, "\n")] = '\0';
            printf("Enter New Semester: ");
            scanf("%d", &s.semester);
            printf("Enter New Year: ");
            scanf("%d", &s.year);

            fwrite(&s, sizeof(s), 1, fp);
            printf("Record updated successfully!\n");
            break;
        }
    }

    if (!found)
        printf("Record not found!\n");

    fclose(fp);
}

void deleteStudent() {
    struct Student s;
    FILE *fp = fopen("students.dat", "rb");
    FILE *temp = fopen("temp.dat", "wb");
    int id, found = 0;

    if (fp == NULL) {
        printf("No records found.\n");
        return;
    }

    printf("Enter Student ID to delete: ");
    scanf("%d", &id);

    while (fread(&s, sizeof(s), 1, fp)) {
        if (s.id != id) {
            fwrite(&s, sizeof(s), 1, temp);
        } else {
            found = 1;
        }
    }

    fclose(fp);
    fclose(temp);

    remove("students.dat");
    rename("temp.dat", "students.dat");

    if (found)
        printf("Record deleted successfully!\n");
    else
        printf("Record not found!\n");
}

int main() {
    int choice;

    do {
        printf("\n--- Student Record Management System ---\n");
        printf("1. Add Student Records\n");
        printf("2. Display Student Records\n");
        printf("3. Update Student Record\n");
        printf("4. Delete Student Record\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                addStudents();
                break;
            case 2:
                displayStudents();
                break;
            case 3:
                updateStudent();
                break;
            case 4:
                deleteStudent();
                break;
            case 5:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice! Please try again.\n");
        }
    } while (choice != 5);

    return 0;
}

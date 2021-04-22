#define _CRT_SECURE_NO_WARNINGS
#include <io.h> // access
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

#define MAX_SIZE 16

void print_usage();
void print_file(char* file);

int main(int argc, char* argv[]) {

	if (argc != 2) {
		print_usage();
	}
	else {

		printf("%s\n", argv[1]);
		if (_access(argv[1], 0x00) == 0) {
			print_file(argv[1]);
		}
		else {
			printf("file not exists\n");
		}

	}

	return 1;

}

void print_usage() {

	printf("\n\ttest.exe [file path]\n");

}

void print_file(char* file) {

	unsigned char buf[MAX_SIZE] = { 0, };
	unsigned char string[MAX_SIZE] = { 0, };
	int offset = 0;
	int cnt = 0;
	FILE* fp = fopen(file, "rb");

	printf("Offset(h)  ");
	for (int i = 0; i < 16; i++) {
		printf("%.2X ", i);
	}
	printf("\n\n");

	while ((cnt = fread(buf, sizeof(char), MAX_SIZE, fp)) != 0) {

		printf("%.8X   ", offset);
		for (int i = 0; i < MAX_SIZE; i++) {

			printf("%.2X ", buf[i]);
			if (0x20 > buf[i] || buf[i] > 0x7F)
				string[i] = '.';
			else
				string[i] = buf[i];

		}

		printf("\t");
		for (int i = 0; i < MAX_SIZE; i++)
			printf("%c", string[i]);

		printf("\n");
		offset += 16;

		memset(buf, 0, MAX_SIZE);
		memset(string, 0, MAX_SIZE);
	}

	fclose(fp);

	return;

}

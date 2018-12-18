#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>

#define MAX 1024
#define MIN(a,b) ((a) < (b) ? (a) : (b))

/* Q: Write your own encryption-decryption algorithm
 * A: Used little endianness of machines with some minor adjustments
 */
int main(int argc, char* argv[]) {
	char msg[MAX], a[12], b[2], *c;

	FILE *f;

	if (argc > 1) {
		f = fopen(argv[1], "r");
		if(f == NULL) {
			perror(argv[1]);
			exit(errno);
		}
	}
	else {
		printf("Usage: ./a.out [filename]");
		exit(0);
	}

	int fd = open("encrypted.txt", O_CREAT | O_WRONLY | O_TRUNC, 0664);
	if(fd == -1) {
		perror("encrypted.txt");
		exit(errno);
	}

	int i = 0, j, fd1, lm = 0;
	int *encmsg;
	char *ptr;
	int l = 0;

	fscanf(f, "%[^\n]%*c", msg); 
	printf("input:\n%s\n\n",msg);
	lm = strlen(msg);
	msg[lm]='\0';
	encmsg = (int*)malloc(lm/4);
	ptr = (char*)encmsg;
	
	for(i = 0; i < lm; i++) {
		*ptr = msg[i];
		ptr++;
	}

	printf("encrypted:\n");
	for(i = 0; i < lm/4 + 1; i++) {
		sprintf(a, "%d", encmsg[i]);
		sprintf(b, "%d", (int)(strlen(a)-1));
		write(fd, &b, strlen(b));
		printf("%s",b);
		write(fd, &a, strlen(a));
		printf("%s",a);
	}
	printf("\n\n");

	l += lm;
	close(fd);
	fclose(f);


	lm = l;

	fd = open("encrypted.txt", O_RDONLY);
	if(fd == -1) {
		perror("encrypted.txt");
		exit(errno);
	}

	fd1 = open("decrypted.txt", O_CREAT | O_WRONLY | O_TRUNC, 0664);
	if(fd1 == -1) {
		perror("decrypted.txt");
		exit(errno);
	}

	printf("output:\n");
	while(read(fd, &b, 1) && lm) {
		i = atoi(b)+1;
		read(fd, &a, i);
		a[i] = '\0';
		i = atoi(a);
		c = (char*)&i;
		j = 0;
		write(fd1, c, 1);
		printf("%c", *c);
		c++;
		lm--;
		while(j < MIN(3,lm) && *c != '\0') {
			write(fd1, c, 1);
			printf("%c", *c);
			j++;
			c++;
		}
		if (*c == '\0') break;
		lm -= 3;
	}
	printf("\n");

	close(fd);
	close(fd1);
	return 0;
}

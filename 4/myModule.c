#include <stdio.h>
#include <Python.h>

#define MAX 256
#define min(a,b) ((a) < (b) ? (a) : (b))

static PyObject* py_encrypt(PyObject* self, PyObject* args) {

	char *msg, a[12], b[2], output[MAX];
	PyArg_ParseTuple(args, "s", &msg);

	int i = 0, lm = 0;
	int *encmsg;
	char *ptr;

	lm = strlen(msg);
	msg[lm]='\0';
	encmsg = (int*)malloc(lm/4);
	ptr = (char*)encmsg;

	for(i = 0; i < lm; i++) {
		*ptr = msg[i];
		ptr++;
	}
	*ptr = '\0';

	output[0]='\0';
	sprintf(a, "%3d", lm);
	i = 0;

	while(i < 3 && a[i] == ' ') a[i++] = '0';

	strcat(output,a);

	for(i = 0; i < lm/4 + 1; i++) {
		sprintf(a, "%d", encmsg[i]);
		sprintf(b, "%d", (int)(strlen(a)-1));
		strcat(output,b);
		strcat(output,a);
	}

	return Py_BuildValue("s", output);
}

static PyObject* py_decrypt(PyObject* self, PyObject* args) {

	char *cipher, msg[MAX];
	PyArg_ParseTuple(args, "s", &cipher);
	int k = 3, i, j, lm;
	char a[12], b[2], *c;

	strncpy(a, cipher, 3);
	a[3] = '\0';
	lm = atoi(a);
	msg[0] = '\0';

	while(lm) {
		b[0] = cipher[k++];
		i = atoi(b)+1;
		strncpy(a, &cipher[k], (size_t)i);
		k += i;
		a[i] = '\0';
		i = atoi(a);
		c = (char*)&i;
		j = 0;
		strncat(msg, c, 1);
		c++;
		lm--;
		while(j < min(3,lm) && *c != '\0') {
			strncat(msg, c, 1);
			j++;
			c++;
		}
		if (*c == '\0') break;
		lm -= 3;
	}
	*c = '\0';

	return Py_BuildValue("s", &msg);
}

static PyMethodDef methods[] = {
    {"encrypt", py_encrypt, METH_VARARGS},
    {"decrypt", py_decrypt, METH_VARARGS},
    {NULL, NULL}
};

static struct PyModuleDef moduledef = {
	PyModuleDef_HEAD_INIT, 
	"myModule",                
	NULL,                  
	-1,                    
	methods           
};

PyMODINIT_FUNC PyInit_myModule(void) {

	PyObject *m;
	m = PyModule_Create(&moduledef);
	return m;
}


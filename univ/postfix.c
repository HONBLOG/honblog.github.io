#include<stdio.h>
#include<stdlib.h>
#include<string.h>

typedef struct Node{
	double data;
	struct Node *link;
}nd;

typedef struct stack{
	nd *top;
}stack;

int get_priority(char op){
	switch(op){
	case '*' : case '/': return 2;
	case '+' : case '-': return 1;
	case '(' : case '{' : case '[' : return 0;
}
return -1;
}

stack* initstack(){
	stack *s = (stack *)malloc(sizeof(stack));
	s->top = NULL;
	return s;
}
int is_empty(stack *s){
	return s->top == NULL;
}

stack* push(stack *s, double data){
	nd* new = (nd*)malloc(sizeof(nd));
	new->data = data;
	new->link = s->top;
	s->top = new;
	return s;
}

double pop(stack *s){
	if(is_empty(s)){
		printf("\nIt's NULL\n");
		return 0;
	}
	nd* temp = s->top;
	double item = s->top->data;
	s->top = s->top->link;
	free(temp);
	return item;
}

double peek(stack *s){
	double item = s->top->data;
	return item;
}

void postfix_convert(stack *s, char *str, char *post){
	int j = 0;
	for(int i = 0; i<strlen(str); i++){
		char ch = str[i];
		switch(ch){
			case '(': case '{': case '[': 
				push(s, (double)ch);
				break;
			case '*': case '/': case '+' : case '-':
				while(!is_empty(s) && get_priority((char)peek(s)) >= get_priority(ch)){
			post[j++] = pop(s);
			}
			push(s, (double)ch);
			break;
			case ')': case '}': case ']':
				char top_op = (char)pop(s);
				while(top_op != '(' && top_op != '{' && top_op != '['){
					post[j++] = top_op;
					top_op = pop(s);
				}
				break;
			default:
				post[j++] = ch;
				break;
		}
		
	}
	while(!is_empty(s)){
			post[j++] = pop(s);
		}
	post[j] = '\0';
}

double postfix_calc(char *post){
	stack *s = initstack();
	double op1, op2;
	for(int i = 0; i < strlen(post); i++){
		char ch=post[i];
		if(ch == '+' || ch == '-' || ch == '*' || ch == '/'){
			op2 = pop(s);
			op1 = pop(s);

			switch(ch){
				case '+' : push(s, op1 + op2); break;
				case '-' : push(s, op1 - op2); break;
				case '*' : push(s, op1 * op2); break;
				case '/' : push(s, op1 / op2); break;
			}
		}
		else if(ch >= '0' && ch <= '9'){
			push(s, ch - '0');
		}
	}
	double result  = pop(s);
	free(s);
	return result;
	return result;
}

int main(){
	char str[100] = {0};
	char post[100] = {0};
	int opt;
	stack *s = initstack();
	while(1){
		printf("\n1. 수식 입력\n2. 포스트픽스 변환기\n3. 포스트픽스 계산기\n4. EXIT\n TYPE >>");
		scanf("%d",&opt);
		if(opt == 4) break;
		switch(opt){
			case(1):
				printf("수식 입력: ");
				scanf("%s",str);
				break;
			case(2):
				postfix_convert(s,str,post);
				printf("\nPOSTFIX => %s\n",post);
				break;
			case(3):
				if(post[0] == '\0'){
					printf("\n변환 후 시도하세요!\n");
					break;
				}
				printf("\nRESULT : %.2f\n", postfix_calc(post));
				break;
			default:
				printf("\n!!!INVALID!!!\n");
				continue;
		}
	}
	free(s);
	return 0;
}

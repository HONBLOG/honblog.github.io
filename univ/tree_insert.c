#include<stdio.h>
#include<stdlib.h>
#include<time.h>

typedef struct Node{
    int data;
    struct Node *left;
    struct Node *right;
}nd;

typedef struct Queue{
    int capacity; int rear; int front;
    nd** arr;
}que;

que* init_queue(int num){
    que* q = (que *)malloc(sizeof(que));
    q->capacity = num;
    q->front = -1;
    q->rear = -1;
    q->arr = (nd**)malloc(q->capacity * sizeof(nd*));
    return q;
}

int is_full(que* q){
    return q->rear == q->capacity - 1;
}

int is_empty(que* q){
    return q->front == q->rear;   
}

que* enqueue(que* q, nd* node){
   if(is_full(q)){
        printf("\nIt's Full!\n");
        return NULL;
   } 
   q->arr[++q->rear] = node;
   return q;
};

nd* dequeue(que* q){
    if(is_empty(q)){
        return NULL;
    }
    return q->arr[++q->front];
} 

nd* make_node(int item){
    nd* new = (nd*)malloc(sizeof(nd));
    new->data = item;
    new->left = NULL;
    new->right = NULL;
    return new;
}

nd* insert_BST(nd* root, int ins, int flag){
    if(root == NULL){
        nd* new = (nd*)malloc(sizeof(nd));
        if(new == NULL){
            printf("\nMEM ERROR\n");
            return NULL;
        }
        else{
            new->data = ins;
            new->left = new->right = NULL;
            root = new;
            if(flag) printf("%d", root->data);
        }
    }
    else{
        if(root->data > ins){
            if(flag){
            printf("%d -> ",root->data);
            }
            root->left = insert_BST(root->left, ins,flag);
        }
        if(root->data < ins){
            if(flag){
            printf("%d -> ", root->data);
            }
             root->right = insert_BST(root->right, ins,flag);
        }
    }
    
    
    return root;
}


nd* randomTree_BST(int num){
    int ran = rand() % 100 + 1;
    nd* root = make_node(ran);
    
    for(int i = 1; i < num; i++){
        ran = rand() % 100 + 1;
        root = insert_BST(root, ran,0);
    }
    return root;
}

void print_inorder(nd* root){
    if(root == NULL){
        return;
    }
    print_inorder(root->left);
    printf("%d ", root->data);
    print_inorder(root->right);
}

void print_levelorder(nd* root, int num){
    if(root == NULL){
        printf("\nNULL\n");
        return;
    }
    que* q = init_queue(num);
    enqueue(q, root);
    int level = 0;

    while(!is_empty(q)){
        int lv = q->rear - q->front;
        printf("\nLEVEL %d : ", level);
        for(int i = 0; i< lv; i++){
        nd* cur = dequeue(q);
        printf("%d ", cur->data);

        if(cur->left != NULL){enqueue(q, cur->left);}
        if(cur->right != NULL){enqueue(q, cur->right);}
        }
        level++;
    }

    free(q->arr);
    free(q);

    return;    
}
int main(){
    srand(time(NULL));
    int num = rand() % 20 + 1;
    int ins;
    nd* root = randomTree_BST(num);

    printf("\n=====IN_ORDER====\n");
    print_inorder(root);
    printf("\n=====LEVEL_ORDER====\n");
    print_levelorder(root, num);
    printf("\n\n삽입할 수 입력 : ");
    scanf("%d", &ins);
    root = insert_BST(root, ins,1);

    return 0;
}

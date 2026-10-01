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

nd* dequeue(que* q){ if(is_empty(q)){
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

nd* findmax(nd* root){
    if(root == NULL){
        return NULL;
    }
    while(root->right != NULL){
        root = root->right;
    }
    return root;
}

nd* findmin(nd* root){
    if(root == NULL){
        return NULL;
    }
    while(root->left != NULL){
        root = root->left;
    }
    return root;
}

nd* delete_BST(nd* root, int del){
    nd* temp;
    if(root == NULL){
        printf("\n\nDOESN'T EXIST\n");
    }
    else if(root->data > del){
        root->left = delete_BST(root->left, del);
    }
    else if(root->data < del){
        root->right = delete_BST(root->right, del);
    }
    else{
        if(root->left != NULL && root->right != NULL){
            temp = findmax(root->left);
            root->data = temp->data;
            root->left = delete_BST(root->left, root->data);
        }
        else{
        temp = root;
        if(root->left == NULL){
            root = root->right;
        }
        else if(root->right == NULL){
            root = root->left;
        }
        free(temp);
        }
    }

    return root;
}

nd* delete_range_BST(nd* root, int d1, int d2){
    if(root == NULL){
        return NULL;
    }
    root->left = delete_range_BST(root->left, d1, d2);
    root->right = delete_range_BST(root->right, d1, d2);

    if(root->data < d1 || root->data > d2){
        root = delete_BST(root, root->data);
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

int search_BST(nd* root, int tar){
    if(root == NULL){
        return 0;
    }
    if(root->data == tar){
        return 1;
    }
    else if(root->data > tar){
        return search_BST(root->left, tar);
    }
    else{
        return search_BST(root->right, tar);
    }
}

int main(){
    srand(time(NULL));
    int num = rand() % 20 + 1;
    int del;
    int try = 1;
    int del_1, del_2;
    nd* root = randomTree_BST(num);

    printf("\n=====IN_ORDER====\n");
    print_inorder(root);
    printf("\n=====LEVEL_ORDER====\n");
    print_levelorder(root, num);
    del = rand() % 100 + 1;
    do{
       del = rand() % 100 + 1;
       try++;
    }while(search_BST(root, del) != 1);
    printf("\n\n%d번 다시 시도함, 삭제할 수 : %d", try, del);
    root = delete_BST(root, del);
    printf("\n=====LEVEL_ORDER====\n");
    print_levelorder(root, num);    
    printf("\n\n삭제할 범위 입력 : ");
    scanf("%d %d", &del_1, &del_2);
    root = delete_range_BST(root, del_1, del_2);
    printf("\n=====LEVEL_ORDER====\n");
    print_levelorder(root, num);

    return 0;
}


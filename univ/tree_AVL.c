#include<stdio.h>
#include<stdlib.h>
#include<time.h>

typedef struct Node{
    int data;
    int height;
    struct Node* left;
    struct Node* right;
}nd;

typedef struct Queue{
    int cap;
    int front;
    int rear;
    nd** arr;
}que;

que* init_queue(int num){
    que* q = (que*)malloc(sizeof(que));
    q->cap = num;
    q->front = -1;
    q->rear = -1;
    q->arr = (nd**)malloc(q->cap * sizeof(nd*));
    return q;
}

nd* init_node(int num){
    nd* new = (nd*)malloc(sizeof(nd));
    new->data = num;
    new->height = 1;
    new->left = NULL;
    new->right = NULL;
    return new;
}

int is_full(que* q){
    return q->rear == q->cap - 1;
}

int is_empty(que* q){
    return q->front == q->rear;
}

que* enqueue(que* q, nd* node){
    if(is_full(q)) return q;
    q->arr[++q->rear] = node;
    return q;
}

nd* dequeue(que* q){
    if(is_empty(q)) return NULL;
    return q->arr[++q->front];
}

int height(nd* node){
    if(node == NULL) return 0;
    return node->height;
}

int max(int a, int b){
    if(a > b) return a;
    else return b;
}

nd* right_rotate(nd* root){
    nd* n_root = root->left;
    nd* temp = n_root->right;

    n_root->right = root;
    root->left = temp;

    root->height = 1 + max(height(root->left),height(root->right));
    n_root->height = 1 + max(height(n_root->left),height(n_root->right));

    return n_root;
}

nd* left_rotate(nd* root){
    nd* n_root = root->right;
    nd* temp = n_root->left;

    n_root->left = root;
    root->right = temp;

    root->height = 1 + max(height(root->left), height(root->right));
    n_root->height = 1 + max(height(root->left), height(root->right));

    return n_root;
}

int balance(nd* root){
    if(root == NULL) return 0;
    else return height(root->left) - height(root->right);
}
// *
nd* insert(nd* root, int data){
    if(root == NULL) return init_node(data);
    else if(root->data < data) root->right = insert(root->right, data);
    else if(root->data > data) root->left = insert(root->left, data);
    else return root;

    root->height = 1 + max(height(root->left), height(root->right));

    int bf = balance(root);
    if(bf > 1){
        if(data < root->left->data){
            printf("*** 발생 노드 : %d, LL이므로 오른쪽회전 ***", root->data);
            root = right_rotate(root); // LL
        }
        if(data > root->left->data){
            printf("*** 발생 노드 : %d, LR이므로 왼쪽->오른쪽회전 ***", root->data);
            root->left = left_rotate(root->left);
            root = right_rotate(root); // LR
            }
    }
    else if(bf < -1){
        if(data > root->right->data){
            printf("*** 발생 노드 : %d, RR이므로 왼쪽회전 ***", root->data);
            root = left_rotate(root); // RR
        }
        if(data < root->right->data){
            printf("*** 발생 노드 : %d, RL이므로 오른쪽->왼쪽회전 ***", root->data);
            root->right = right_rotate(root->right);
            root = left_rotate(root); // RL
        }
    }
    return root;
}

int check_avl(nd* root){
    if(balance(root) >= -1 && balance(root) <= 1) return 1;
    else return 0;
}

void print_level(nd* root, int num){
    if(root == NULL) return;
    que* q = init_queue(num);
    q = enqueue(q, root);
    int lv = 0;
    while(!is_empty(q)){
        int num = q->rear - q->front;
        nd* temp = NULL;
        printf("\n=====LEVEL : %d=====\n", lv);
        for(int i = 0; i < num; i++){
            temp = dequeue(q);
            printf("%d ", temp->data);
            if(temp->left != NULL) enqueue(q, temp->left);
            if(temp->right != NULL) enqueue(q, temp->right);
        }
        lv++;
    }
    free(q->arr);
    free(q);
}

void print_tree(nd* root, int num){
    if(root == NULL) return;

    print_tree(root->right, num + 1);

    for(int i = 0; i < num; i++) printf("   ");
    printf("[%d]\n", root->data);

    print_tree(root->left, num + 1);
}

void free_tree(nd* root){
    if(root == NULL) return;

    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

int main(){
    srand(time(NULL));
    int data, num;
    nd* root = NULL;

    printf("\nTYPE A NUM OF NODES : ");
    scanf("%d", &num);

    for(int i = 0; i < num; i++){
        printf("\nType a Node : ");
        scanf("%d", &data);
        root = insert(root, data);
    }
    printf("\n==========PRINT============");
    print_level(root, num);
    printf("\n");
    print_tree(root, 0);
    printf("==========QUIT=============\n");
    printf("++++CHECK_AVL++++\n");
    if(check_avl(root)) printf("정상적인 AVL입니다!");
    else printf("정상적인 AVL이 아님!");
    free_tree(root);
    return 0;
}

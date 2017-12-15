
int sum(int _a, int _b) {return _a + _b;}

int ret10(void) {return 10;}

int main() {return sum(ret10(), ret10());}

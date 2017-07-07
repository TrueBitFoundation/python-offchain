
int sum(int __1, int __2)
{
  return(__1 + __2);
}

int main (int argc, char** argv)
{
  int (*sum_pointer)(int, int);

  sum_pointer = &sum;

  return sum_pointer(10, 10);
}

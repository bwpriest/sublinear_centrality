#include <cmath>
#include <iostream>

using namespace std;

// Implements sampling and applying a hash function 
// h: [u_dom] -> [u_ran] from a 2-universal family 
// using the multiply-add-shift scheme. 
class TwoUnivHash
{
public:
  TwoUnivHash(unsigned int, unsigned int, unsigned int, 
	    unsigned int);
  void members();
  unsigned int hash(unsigned int);
private:
  unsigned int trunc;
  unsigned int u_dom;
  unsigned int u_ran;
  unsigned int mul;
  unsigned int add;
};

TwoUnivHash::TwoUnivHash(unsigned int a, unsigned int b, 
		     unsigned int n, unsigned int m)
{
  mul = a;
  add = b;
  u_dom = n;
  u_ran = m;
  trunc = std::pow(2,n)-1;
}

void TwoUnivHash::members()
{
  std::cout << "mul is " << mul << std::endl;    
  std::cout << "add is " << add << std::endl;
  std::cout << "u_dom is " << u_dom << std::endl;
  std::cout << "u_ran is " << u_ran << std::endl;
  std::cout << "trunc is " << trunc << std::endl;
}

unsigned int TwoUnivHash::hash(unsigned int x)
{
  return (unsigned) ((mul*x + add) & trunc) >> (u_dom - u_ran);
}

// Define C functions for the C++ class - as ctypes can only talk to C...
extern "C"
{
  TwoUnivHash* TwoUnivHash_new(unsigned int a, unsigned int b, 
			   unsigned int n, unsigned int m) 
  {
    return new TwoUnivHash(a,b,n,m);
  }
  void TwoUnivHash_members(TwoUnivHash* f) { f->members();}
  unsigned int TwoUnivHash_hash(TwoUnivHash* f, unsigned int x) { return f->hash(x);}
}

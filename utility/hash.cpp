#include <cmath>
#include <iostream>

using namespace std;

typedef unsigned long ulong;

// Implements sampling and applying a hash function 
// h: [u_dom] -> [u_ran] from a 2-universal family 
// using the multiply-add-shift scheme. 
class TwoUnivHash
{
public:
  TwoUnivHash(ulong, ulong, ulong, ulong);
  void members();
  ulong hash(ulong);
private:
  ulong trunc;
  ulong u_dom;
  ulong u_ran;
  ulong mul;
  ulong add;
};

TwoUnivHash::TwoUnivHash(ulong a, ulong b, ulong n, ulong m)
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

ulong TwoUnivHash::hash(ulong x)
{
  return (unsigned) ((mul*x + add) & trunc) >> (u_dom - u_ran);
}

// Define C functions for the C++ class - as ctypes can only talk to C...
extern "C"
{
  TwoUnivHash* TwoUnivHash_new(ulong a, ulong b, ulong n, ulong m) 
  {
    return new TwoUnivHash(a,b,n,m);
  }
  void TwoUnivHash_members(TwoUnivHash* f) { f->members();}
  ulong TwoUnivHash_hash(TwoUnivHash* f, ulong x) { return f->hash(x);}
}

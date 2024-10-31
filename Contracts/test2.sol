pragma solidity >=0.4.22 <0.6.0;
contract Sample{
   struct Student { 
      uint age;
   }
    Student student = Student(32);
    mapping(uint => uint) public prices;
    uint[10] balance;
    uint[][][] temp = [[[2,4],[3,6]],[[2,4],[3,6]]];

function  fun2(uint a, uint b)
    pure  public  returns(uint){
	    uint c = a + b;
	    uint d = b + b + a + a;
         return d + c;
    }

function  issue1(uint a, uint b, uint c)
    pure  public  returns(uint){
        uint d; uint e; uint f; uint g; uint h;
        d = c +  b * a +  a * b;
        e = a * b + c;
        f = a * b + b * a;
        //{
	//	uint a = 4;
	 //  } 
	  g = b * a;
        h = e + f + g;
        return d + h;
    }
    
function  fun1(uint a, uint b, uint c)
    public  returns(uint){
	   uint a1 = b + c;
	   balance[c] = b + a + c + balance[c + b];
        uint e = c + balance[b]+ temp[b][c][c];
	   uint d = student.age;
	   d = b + student.age;
	   e = prices[2] + prices[balance[b]+d + c+temp[b][c][c]];
	   a = fun2(b, c);
	   uint b1 = b + fun2(b, c) + c;
	   uint c1 = uint(a);
	   uint d1 = uint(fun2(b, c));	
        return a + e;
    }

function  issue2(uint a, uint b, uint c)
    pure  public  returns(uint){
        uint d; uint e; uint f; uint g; uint h;
        d = c +  b * a +  a * b;
        e = a * b + c;
        f = a * b + b * a;
        g = b * a;
        h = e + f + g;
	  do{
		a = c;
		d = c +  b * a +  a * b;
	      e = a * b + c;
     	  	 f = a * b + b * a;
     		 g = b * a;
        	h = e + f + g;
	  }while(f>g);

        return d + h;
    }

}


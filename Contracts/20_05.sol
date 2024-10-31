pragma solidity >=0.4.22 <0.6.0;
contract Sample{
function  issue2(uint a, uint b, uint c)
    pure  public  returns(uint){
        uint d; uint e; uint f; uint g; uint h;
        d = c +  b * a +  a * b;
        e = a * b + c;
        f = a * b + b * a;
        g = b * a;
        h = e + f + g;
	  do{
		a = g;
		d = h +  b * a +  a * b;
	      e = a * b + c;
     	  	 f = a * b + b * a;
     		 g = b * a;
        	h = e + f + g;
	  }while(f>g);

        return d + h;
    }

}

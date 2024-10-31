import java.util.Random;

public class Account {
    private String address;
    private float balance;

    public Account(String address, float balance) {
        this.address = address;
        this.balance = balance;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public float getBalance() {
        return balance;
    }

    public void setBalance(float balance) {
        this.balance = balance;
    }

    @Override
    public String toString() {
        return "Address: " + address + ", Balance: " + balance;
    }

    // Global variables
    //static float gas_to_be_used;
    //static boolean gas_exhausted;

    public boolean approximate(float amount) {
        float gas_to_be_used;
        boolean gas_exhausted;
        
        Random rand1 = new Random();
        gas_to_be_used = rand1.nextFloat() * 3000 + 1;
        System.out.println("Gas to be used is "+ gas_to_be_used);

        // Generate random value for gas_exhausted (1 in 5 chance of being true)
        gas_exhausted = (rand1.nextInt(5) + 1) == 1;
        
        if (gas_exhausted) {
            System.out.println("Gas exhausted");
            return false;
        } else if (gas_to_be_used >= 2300) {
            System.out.println("Gas usage is going above 2300");
            return false;
        } else {
            Random rand = new Random();
            int random1 = rand.nextInt(10); // First random number between 0 and 9
            int random2;
            do {
                random2 = rand.nextInt(10); // Generate second random number until it's different from the first
            } while (random2 == random1);

            // Access instances of Account using random numbers
            Account senderAccount = accounts[random1];
            Account receiverAccount = accounts[random2];

            float sender_balance = senderAccount.getBalance();
            float receiver_balance = receiverAccount.getBalance();

            System.out.println("Random numbers: " + random1 + " and " + random2);
            System.out.println("Sender balance: " + sender_balance);
            System.out.println("Receiver balance: " + receiver_balance);

            if (amount > sender_balance) {
                System.out.println("Insufficient balance in sender's account");
                return false;
            } else {
                // Update balances and print transaction details
                receiver_balance += amount;
                sender_balance -= amount;

                System.out.println("Transaction successful");
                System.out.println("Final sender balance: " + sender_balance);
                System.out.println("Final receiver balance: " + receiver_balance);

                // Update gas_to_be_used
                gas_to_be_used += 50.0f; // Example adjustment

                return true;
            }
        }
    }

    public boolean send(float amount) {
        return approximate(amount);
    }

    public boolean transfer(float amount) {
        boolean result = approximate(amount);
        if (!result) {
            System.out.println("Exception on transfer");
        }
        return result;
    }

    private static Account[] accounts = new Account[10]; // Array of Account instances

    public static void main(String[] args) {
        // Create 10 Account instances with sample data
        accounts[0] = new Account("0x123456789abcdef0123456789abcdef0123456789", 1000.0f);
        accounts[1] = new Account("0xabcdef0123456789abcdef0123456789abcdef012", 2500.0f);
        accounts[2] = new Account("0x9876543210abcdef0123456789abcdef01234567", 150.0f);
        accounts[3] = new Account("0xfedcba9876543210abcdef0123456789abcdef012", 3000.0f);
        accounts[4] = new Account("0xabcdef0123456789abcdef0123456789abcdef012", 500.0f);
        accounts[5] = new Account("0x0123456789abcdef0123456789abcdef01234567", 1200.0f);
        accounts[6] = new Account("0xfedcba9876543210abcdef0123456789abcdef012", 750.0f);
        accounts[7] = new Account("0x123456789abcdef0123456789abcdef0123456789", 2000.0f);
        accounts[8] = new Account("0x9876543210abcdef0123456789abcdef01234567", 1800.0f);
        accounts[9] = new Account("0xabcdef0123456789abcdef0123456789abcdef012", 900.0f);

        // Create an instance of Account for calling the send and transfer functions
        Account accountInstance = new Account("", 0.0f);

        // Call the send function with a sample amount
        boolean sendStatus = accountInstance.send(500.0f);
        System.out.println("Send status: " + sendStatus);

        // Call the transfer function with a sample amount
        boolean transferStatus = accountInstance.transfer(700.0f);
        System.out.println("Transfer status: " + transferStatus);
    }
}
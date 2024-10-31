import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class BlockchainSimulator {

    // Simulated blockchain environment state variables
    private Instant currentBlockTimestamp;
    private long currentBlockGasLimit;
    private final Map<String, Account> accounts; // Store account balances for simulation

    // Default gas limit (can be customized)
    private static final long DEFAULT_GAS_LIMIT = 8000000;

    // Constructor
    public BlockchainSimulator() {
        this.currentBlockTimestamp = Instant.now();
        this.currentBlockGasLimit = DEFAULT_GAS_LIMIT;
        this.accounts = new HashMap<>();
    }

    // Class to simulate an account on the blockchain
    public static class Account {
        private String address;
        private long balance;

        public Account(String address, long balance) {
            this.address = address;
            this.balance = balance;
        }

        public String getAddress() {
            return address;
        }

        public long getBalance() {
            return balance;
        }

        public void addBalance(long amount) {
            this.balance += amount;
        }

        public boolean deductBalance(long amount) {
            if (this.balance >= amount) {
                this.balance -= amount;
                return true;
            }
            return false; // Not enough balance
        }
    }

    // Get the current block timestamp
    public Instant getCurrentBlockTimestamp() {
        return currentBlockTimestamp;
    }

    // Set a new block timestamp to simulate time passage
    public void mineNewBlock() {
        this.currentBlockTimestamp = this.currentBlockTimestamp.plusSeconds(15);
        System.out.println("New block mined at timestamp: " + currentBlockTimestamp);
    }

    // Get the current block gas limit
    public long getCurrentBlockGasLimit() {
        return currentBlockGasLimit;
    }

    // Set a new gas limit for the block
    public void setCurrentBlockGasLimit(long gasLimit) {
        this.currentBlockGasLimit = gasLimit;
    }

    // Add a new account to the simulator
    public void addAccount(String address, long initialBalance) {
        this.accounts.put(address, new Account(address, initialBalance));
    }

    // Get an account by address
    public Account getAccount(String address) {
        return accounts.get(address);
    }

    // Transfer funds between accounts
    public boolean transfer(String fromAddress, String toAddress, long amount) {
        Account fromAccount = accounts.get(fromAddress);
        Account toAccount = accounts.get(toAddress);

        if (fromAccount != null && toAccount != null && fromAccount.deductBalance(amount)) {
            toAccount.addBalance(amount);
            System.out.println("Transfer of " + amount + " units from " + fromAddress + " to " + toAddress);
            return true;
        }
        System.out.println("Transfer failed: Insufficient funds or invalid account.");
        return false;
    }

    // Generate a random new account with a unique address and random balance
    public String createRandomAccount() {
        String address = "0x" + Integer.toHexString(new Random().nextInt());
        long balance = new Random().nextInt(100000);
        addAccount(address, balance);
        System.out.println("New account created: " + address + " with balance: " + balance);
        return address;
    }
}

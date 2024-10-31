import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;

public class TransactionContext {
    
    // Simulate the blockchain addresses and their balances
    private static Map<String, BigDecimal> addressBalances = new HashMap<>();
    
    // Attributes to represent transaction context
    private String sender;
    private BigDecimal value;

    // Constructor for initializing a transaction context
    public TransactionContext(String sender, BigDecimal value) {
        this.sender = sender;
        this.value = value;
    }
    
    // Static initializer block to set initial balances for testing
    static {
        // Initialize some addresses with starting balances
        addressBalances.put("0xSenderAddress1", new BigDecimal("100.0"));
        addressBalances.put("0xSenderAddress2", new BigDecimal("50.0"));
        // Add more as necessary
    }

    // Get the sender's address (equivalent to msg.sender in Solidity)
    public String getSender() {
        return sender;
    }

    // Get the transaction value (equivalent to msg.value in Solidity)
    public BigDecimal getValue() {
        return value;
    }

    // Method to get the balance of a specific address
    public static BigDecimal getBalance(String address) {
        return addressBalances.getOrDefault(address, BigDecimal.ZERO);
    }

    // Method to simulate transferring ether between addresses
    public static void transfer(String from, String to, BigDecimal amount) throws Exception {
        if (!addressBalances.containsKey(from)) {
            throw new Exception("Sender address not found.");
        }
        if (!addressBalances.containsKey(to)) {
            throw new Exception("Receiver address not found.");
        }
        BigDecimal senderBalance = addressBalances.get(from);
        if (senderBalance.compareTo(amount) < 0) {
            throw new Exception("Insufficient balance.");
        }
        // Deduct from sender
        addressBalances.put(from, senderBalance.subtract(amount));
        // Add to receiver
        addressBalances.put(to, addressBalances.get(to).add(amount));
    }

    // Method to add funds to an address (for testing purposes)
    public static void deposit(String address, BigDecimal amount) {
        addressBalances.put(address, addressBalances.getOrDefault(address, BigDecimal.ZERO).add(amount));
    }

    // Method to simulate the transaction initiation process
    public static TransactionContext initiateTransaction(String sender, BigDecimal value) {
        return new TransactionContext(sender, value);
    }
    
    // Test utility to display all balances (for debugging)
    public static void displayBalances() {
        System.out.println("Balances:");
        addressBalances.forEach((address, balance) -> {
            System.out.println(address + ": " + balance + " ETH");
        });
    }

    // Example of how this class would be used
    public static void main(String[] args) {
        try {
            // Display initial balances
            displayBalances();

            // Initiate a transaction
            TransactionContext tx = initiateTransaction("0xSenderAddress1", new BigDecimal("10.0"));

            // Transfer 10 ETH from SenderAddress1 to SenderAddress2
            transfer(tx.getSender(), "0xSenderAddress2", tx.getValue());

            // Display updated balances
            displayBalances();

        } catch (Exception e) {
            System.out.println("Transaction failed: " + e.getMessage());
        }
    }
}

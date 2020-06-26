# CTFd-Fox
[Chinese version](github.com/publicqi/CTFd-Fox/blob/master/README-zh.md)

**Updated: It's stupid to use the same address for on Blockchian challenge as people definitely will steal exploits from other transactions. This repo has been abandoned.**

No more static flags for smart contract challenges!

There're some challenges store the static flag in the contract, allowing players to view it straightforward. This CTFd plugin avoids that! It requires only one more function in the contract (see [example.sol](github.com/publicqi/CTFd-Fox/blob/master/example.sol)).

---

### Installation

1. Clone the repository and place them under `plugins` directory.
2. `pip install web3`
3. Set your own HTTPProvider in `address_flag/web3utils.py`. **Infura** is an excellent one. Be sure you used the correct network (for most cases, Ropsten)

---

### How to create a challenge?

1. Create a challenge using type **smart contract** and no need to set flag at this stage
2. Go to **challenge**, select **Flags**, and create a flag with type **address**
3. Fill in the address of the contract

---

### How to submit flag and how is flag judged?

Instead of typical getFlag() functions, you need to implement a **leaveMsg()**.

[example.sol](github.com/publicqi/CTFd-Fox/blob/master/example.sol)

It's similar to a getFlag function: If the condition mets, the sender can leave a message to the Ethereum chain. Players need to submit the **transaction hash **for this function call. [web3utils.py](github.com/publicqi/CTFd-Fox/blob/master/address_flag/web3utils.py) checks if the **transaction is success** and the **message matches the user's email**.

That is, after the user achieved some requests, the player needs to send a message contains his/her own email address and submit the transaction hash.

---

### Own function header

There's a check in [web3utils.py](github.com/publicqi/CTFd-Fox/blob/master/address_flag/web3utils.py) that the function header matches the expected one. You can edit `func_header` to name your own checker function.

---

### TODO

- Use uuid instead of email
- Challenge specific func_header


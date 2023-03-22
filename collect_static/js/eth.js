
async function write_to_Dapp() {
    const contractABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"player","type":"address"},{"internalType":"string","name":"tokenURI","type":"string"}],"name":"mint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    const contractAddress = "0x7f331fcb6a314400686abbc40c51db200535dc79";
    const contract_privatekey = "77599fb2f4f22ec02ac80798a27843c05ec283372e919e570182ef955976027a"
    const info_returns = 'http://www.alldio.xyz/dapps_return'

    const provider = new ethers.providers.Web3Provider(window.ethereum)
    const signer = new ethers.Wallet(contract_privatekey, provider);
    const contract = new ethers.Contract(contractAddress, contractABI, signer);
    const accounts = await provider.send("eth_requestAccounts", []);

    // mint contract
    const instance = await contract.mint(accounts[0], info_returns)
    console.log('song mint success', instance)

}

write_to_Dapp()


// send transaction
    // const tx = {
    //     to: accounts[0],
    //     value: ethers.utils.parseEther("0.002"),
    //     type: 1,
    //     gasPrice: await provider.getGasPrice(),
    //     gasLimit: ethers.utils.hexlify(21000),
    // };
    // signer.sendTransaction(tx)

    // // let varGasPrice = ethers.getGasPrice();
    // console.log(varGasPrice, '...')

    // console.log(parseInt(await provider.getGasPrice()))

    // const sendTransactionPromise = await signer.sendTransaction(tx);
    // console.log(sendTransactionPromise)



// async function connect_to_metamask() {
//     //向钱包发送授权请求
//     const accounts = await provider.send("eth_requestAccounts", []);
//
//     //获取账户余额信息
//     if (accounts && accounts.length > 0) {
//         let myAccountAddr = accounts[0];
//         let balance = ethers.utils.formatEther(await provider.getBalance(myAccountAddr));
//         let network = await provider.getNetwork();
//         //显示在界面上；
//         document.getElementById('txt_curent_addr').innerText = myAccountAddr;
//         document.getElementById('txt_balance').innerText = balance;
//         // console.log("当前账户地址：", myAccountAddr);
//         // console.log("金额：", balance);
//         // console.log("Chain Info;", network.chainId, network.name);
//     }
// }


// async function connect_to_Dapp() {
//     const BlockNumber = await provider.getBlockNumber();
//     console.log(BlockNumber);
//
//     // 获取当前主账户
//     let privateKey = "77599fb2f4f22ec02ac80798a27843c05ec283372e919e570182ef955976027a";
//     let wallet = new ethers.Wallet(privateKey, provider);
//     let accountAddress = wallet.address;
//     console.log('address:', accountAddress);
//
//     // 获取账户余额（通过地址或 ENS 名称，如果网络支持）
//     const balance = await provider.getBalance(accountAddress);
//     console.log('wei:', balance.toString());  // 84878281540000000000 Wei
//
//     // 余额格式化（ether与wei的转换）
//     console.log('ether:', ethers.utils.formatEther(balance.toString())); // 84.87828154 Ether'
//
//     write_to_Dapp()
// }
//
// connect_to_Dapp()
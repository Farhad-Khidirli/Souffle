let contract = artifacts.require("SendEther");

module.exports = function(deployer) {
    deployer.deploy(contract);
};

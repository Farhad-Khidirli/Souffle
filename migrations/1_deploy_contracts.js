var test = artifacts.require("Greeter");

module.exports = function(deployer) {
    deployer.deploy(test);
};

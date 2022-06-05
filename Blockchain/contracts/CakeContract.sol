// SPDX-License-Identifier: CC-BY-SA-4.0
pragma solidity >= 0.5.0 < 0.9.0;

contract CakeContract {

  struct IPFSInfo {
    bytes32 hashPart1;
    bytes32 hashPart2;
  }
  mapping (uint64 => IPFSInfo) allLinks;

  struct userInfo {
    uint[] attributes;
  }
  mapping (address => userInfo) allUsers;

  function setIPFSInfo(uint64 _caseID, bytes32 _hash1, bytes32 _hash2) public {
    allLinks[_caseID].hashPart1 = _hash1;
    allLinks[_caseID].hashPart2 = _hash2;
  }

  function getIPFSInfo(uint64 _caseID) public view returns (bytes memory) {
    bytes32 p1 = allLinks[_caseID].hashPart1;
    bytes32 p2 = allLinks[_caseID].hashPart2;
    bytes memory joined = new bytes(64);
    assembly {
      mstore(add(joined, 32), p1)
      mstore(add(joined, 64), p2)
    }
    return joined;
  }

  function setUserInfo(address _address, uint[] memory _attributes) public {
    allUsers[_address].attributes = _attributes;
  }

  function getUserInfo(address _address) public view returns (uint[] memory) {
    return allUsers[_address].attributes;
  }

}

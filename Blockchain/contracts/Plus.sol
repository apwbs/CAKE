// SPDX-License-Identifier: CC-BY-SA-4.0
pragma solidity >= 0.5.0 < 0.9.0;

contract Plus {

  struct IPFSInfo {
    string link;
  }
  mapping (uint => IPFSInfo) AllLinks;

  struct UserInfo {
    uint[] attributes;
  }
  mapping (address => UserInfo) AllUsers;

  function setUserInfo(address Address, uint[] memory _attributes) public {
    AllUsers[Address].attributes= _attributes;
  }

  function getUserInfo(address Address) public view returns (uint[] memory) {
    return AllUsers[Address].attributes;
  }

  function setIPFSInfo(uint64 CaseID, string memory _link) public {
    AllLinks[CaseID].link= _link;
  }

  function getIPFSInfo(uint64 CaseID) public view returns (string memory) {
    return AllLinks[CaseID].link;
  }

}

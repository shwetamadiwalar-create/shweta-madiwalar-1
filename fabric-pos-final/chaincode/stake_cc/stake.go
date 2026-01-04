package main

import (
    "encoding/json"
    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type StakeContract struct {
    contractapi.Contract
}

type StakeRecord struct {
    Stake int `json:"stake"`
    Flag  string `json:"flag"`
}

func (s *StakeContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
    initial := map[string]StakeRecord{
        "Org1": {Stake: 10, Flag: "OK"},
        "Org2": {Stake: 10, Flag: "OK"},
    }
    data, _ := json.Marshal(initial)
    return ctx.GetStub().PutState("stakeTable", data)
}

func (s *StakeContract) UpdateStake(ctx contractapi.TransactionContextInterface, peer string, delta int, flag string) error {
    tableBytes, _ := ctx.GetStub().GetState("stakeTable")
    var table map[string]StakeRecord
    json.Unmarshal(tableBytes, &table)

    record := table[peer]
    record.Stake += delta
    record.Flag = flag
    table[peer] = record

    newBytes, _ := json.Marshal(table)
    return ctx.GetStub().PutState("stakeTable", newBytes)
}

func (s *StakeContract) GetStake(ctx contractapi.TransactionContextInterface, peer string) (int, error) {
    tableBytes, _ := ctx.GetStub().GetState("stakeTable")
    var table map[string]StakeRecord
    json.Unmarshal(tableBytes, &table)

    return table[peer].Stake, nil
}

func main() {
    chaincode, _ := contractapi.NewChaincode(new(StakeContract))
    chaincode.Start()
}

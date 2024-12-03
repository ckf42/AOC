#ifndef AOC_UTIL_H
#define AOC_UTIL_H

#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

#include <cpr/api.h>
#include <cpr/cpr.h>
#include <cpr/cprtypes.h>
#include <cpr/response.h>

namespace util{
inline std::string getInput(int year, int day){
    std::string inputFileName = "input" + std::to_string(day);
    if (!std::filesystem::exists(inputFileName)){
        std::cout << "Fetching input ..." << std::endl;
        std::ifstream tokenFile("../session");
        if (!tokenFile){
            throw std::runtime_error("Token file not found");
        }
        std::ofstream outFile(inputFileName);
        if (!outFile){
            throw std::runtime_error("Cannot write to input file");
        }
        std::stringstream buff;
        buff << tokenFile.rdbuf();
        std::string tokenString(buff.str());
        cpr::Response r = cpr::Get(
            cpr::Url{
                "https://adventofcode.com/" 
                + std::to_string(year) 
                + "/day/" + std::to_string(day) 
                + "/input"
            },
            cpr::Header{
                {"Cookie", "session=" + tokenString},
                {"User-Agent", "github.com/ckf42"}
            }
        );
        outFile << r.text;
    }
    std::ifstream inputFile(inputFileName);
    if (!inputFile){
        throw std::runtime_error("Unable to read input file");
    }
    std::stringstream inputBuff;
    inputBuff << inputFile.rdbuf();
    return inputBuff.str();
}

inline std::vector<std::string> splitline(const std::string &s){
    std::vector<std::string> res;
    std::stringstream ss(s);
    std::string buff;
    while (std::getline(ss, buff, '\n')){
        res.push_back(buff);
    }
    return res;
}

inline std::vector<int> getInts(const std::string &s){
    std::vector<int> res;
    std::stringstream ss(s);
    int buff;
    while (ss >> buff){
        res.push_back(buff);
    }
    return res;
}

};  // namespace util

#endif

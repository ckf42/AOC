#ifndef AOC_UTIL_H
#define AOC_UTIL_H

#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace util{
inline std::string getInput(int year, int day){
    std::string inputFilePath = "../" + std::to_string(year) + "/input" + std::to_string(day);
    if (!std::filesystem::exists(inputFilePath)){
        throw std::runtime_error("Input file not found");
    }
    std::ifstream inputFile(inputFilePath);
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

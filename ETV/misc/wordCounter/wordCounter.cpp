#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <queue>


using namespace std;

using TOKEN = string;

void counter(ifstream &in, unordered_map<TOKEN, int> &mapa, vector<TOKEN>& tokens) {
	TOKEN tok;
	int value;
	while (!in.eof()) {
		in >> tok;
		value = 0;
		auto itr = mapa.find(tok);
		if (itr != mapa.end())
			value = itr->second;
		else
			tokens.push_back(tok);

		mapa[tok] = value + 1;
		
	}


}

void nFirst(int n, unordered_map<TOKEN, int> &mapa, vector<TOKEN> &tokens, ofstream &out) {
	priority_queue<pair<int, TOKEN>> pq = priority_queue<pair<int, TOKEN>>();

	for (int i = 0; i < tokens.size(); ++i) {
		pq.push(pair<int, TOKEN>(mapa.find(tokens[i])->second, tokens[i]));
	}

	for (int i = 0; i < n && i < tokens.size(); ++i) {
		out << pq.top().second << "\n";
		pq.pop();
	}
}

void countWords(string pathin, string pathout, int n) {
	ifstream in;
	ofstream out;
	in.open(pathin);
	if (!in.is_open())
		exit(1);
	out.open(pathout);
	if (!out.is_open())
		exit(1);
	unordered_map<TOKEN, int> mapa = unordered_map<TOKEN, int>();
	vector<TOKEN> tokens = vector<TOKEN>();


	counter(in, mapa, tokens);
	nFirst(n, mapa, tokens, out);

	in.close();
	out.close();

}
// inPath outPath nWords
int main(int argc, char*argv[]) {

	string in, out;
	in = argv[1];
	out = argv[2];
	int n = stoi(argv[3]);
	

	countWords(in, out, n);

	return 0;
}
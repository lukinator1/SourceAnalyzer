#include "pch.h"
#include "Image.h"
#include <iostream>
#include <fstream>
using namespace std;
void test(Image firstimage, Image secondimage, int tasknumber);
int main()
{
	Image layer1;
	Image layer2;
	Image pattern1;
	Image pattern2;
	Image car;
	Image text;
	Image circles;
	Image layerred;
	Image layergreen;
	Image layerblue;
	Image temptask;
	Image text2;
	Image task1;
	Image task2;
	Image task3;
	Image task4;
	Image task5;
	Image task6;
	Image task7;
	Image task8g;
	Image task8r;
	Image task8b;
	Image task9;
	Image task10;
	Image extracredit;
	Image example1;
	Image example2;
	Image example3;
	Image example4;
	Image example5;
	Image example6;
	Image example7;
	Image example8b;
	Image example8g;
	Image example8r;
	Image example9;
	Image example10;

	extracredit.imagedata.resize(1048576);
	extracredit.width = 1024;
	extracredit.height = 1024;

	layer1.setdata("input\\layer1.tga");
	layer2.setdata("input\\layer2.tga");
	pattern1.setdata("input\\pattern1.tga");
	car.setdata("input\\car.tga");
	pattern2.setdata("input\\pattern2.tga");
	text.setdata("input\\text.tga");
	circles.setdata("input\\circles.tga");
	text2.setdata("input\\task2.tga");

	example1.setdata("examples\\EXAMPLE_part1.tga");
	example2.setdata("examples\\EXAMPLE_part2.tga");
	example3.setdata("examples\\EXAMPLE_part3.tga");
	example4.setdata("examples\\EXAMPLE_part4.tga");
	example5.setdata("examples\\EXAMPLE_part5.tga");
	example6.setdata("examples\\EXAMPLE_part6.tga");
	example7.setdata("examples\\EXAMPLE_part7.tga");
	example8b.setdata("examples\\EXAMPLE_part8_b.tga");
	example8g.setdata("examples\\EXAMPLE_part8_g.tga");
	example8r.setdata("examples\\EXAMPLE_part8_r.tga");
	example9.setdata("examples\\EXAMPLE_part9.tga");
	example10.setdata("examples\\EXAMPLE_part10.tga");


	task1.multiply(layer1, pattern1);
	task1.writefile("output\\part1.tga");
	test(task1, example1, 1);

	task2.subtract(car, layer2);
	task2.writefile("output\\part2.tga");
	test(task2, example2, 2);

	temptask.multiply(layer1, pattern2);
	task3.screen(temptask, text);
	task3.writefile("output\\part3.tga");
	test(task3, example3, 3);

	temptask.multiply(layer2, circles);
	task4.subtract(temptask, pattern2);
	task4.writefile("output\\part4.tga");
	test(task4, example4, 4);

	task5.overlay(layer1, pattern1);
	task5.writefile("output\\part5.tga");
	test(task5, example5, 5);

	task6.setdata("input\\car.tga");
	task6.addcolor("green", 200);
	task6.writefile("output\\part6.tga");
	test(task6, example6, 6);

	car.setdata("input\\car.tga");
	car.scalered();
	car.writefile("output\\part7.tga");
	task7.setdata("output\\part7.tga");
	test(task7, example7, 7);

	car.setdata("input\\car.tga");
	car.writecolor("output\\part8_b.tga", "blue");
	car.writecolor("output\\part8_g.tga", "green");
	car.writecolor("output\\part8_r.tga", "red");
	task8g.setdata("output\\part8_g.tga");
	task8r.setdata("output\\part8_r.tga");
	task8b.setdata("output\\part8_b.tga");
	test(task8g, example8g, 8);
	test(task8r, example8r, 8);
	test(task8b, example8b, 8);

	layergreen.setdata("input\\layer_green.tga");
	layerblue.setdata("input\\layer_blue.tga");
	task9.setdata("input\\layer_red.tga");
	task9.implementcolors(layergreen, "green");
	task9.implementcolors(layerblue, "blue");
	task9.writefile("output\\part9.tga");
	test(task9, example9, 9);
	
	text2.setdata("input\\text2.tga");
	text2.flipandwrite("output\\part10.tga");
	task10.setdata("output\\part10.tga");
	test(task10, example10, 10);

	/*car.setdata("car.tga");
	circles.setdata("circles.tga");
	text.setdata("text.tga");
	pattern1.setdata("pattern1.tga");*/
}
void test(Image firstimage, Image secondimage, int tasknumber) {
	bool testspassed = true;
	if (firstimage.imagedata.size() != secondimage.imagedata.size()) {
		cout << "Size of the image is different, task " << tasknumber << " failed." << endl;
		testspassed = false;
	}
	int counter = 0;
	for (unsigned int i = 0; i < (firstimage.width * secondimage.height); i++) {	
		if (firstimage.imagedata[i].green != secondimage.imagedata[i].green) {
			cout << "Green is different, task " << tasknumber << " failed on pixel " << i << " ." << endl;
			cout << "My green: " << (int)firstimage.imagedata[i].green << ", their green: " << (int)secondimage.imagedata[i].green << endl;
			testspassed = false;
			counter++;
		}
		if (firstimage.imagedata[i].red != secondimage.imagedata[i].red) {
			cout << "Red is different, task " << tasknumber << " failed on pixel " << i << " ." << endl;
			cout << "My red: " << (int)firstimage.imagedata[i].red << ", their red: " << (int)secondimage.imagedata[i].red << endl;
				testspassed = false;
			counter++;
		}
		if (firstimage.imagedata[i].blue != secondimage.imagedata[i].blue) {
			cout << "Blue is different, task " << tasknumber << " failed on pixel " << i << " ." << endl;
			cout << "My blue: " << (int)firstimage.imagedata[i].blue << ", their green: " << (int)secondimage.imagedata[i].blue << endl;
			testspassed = false;
			counter++;
		}
		if (counter >= 10) {
			cout << "Too many errors! Go back and fix them." <<endl;
			counter = 0;
			break;
		}
	}
	if (testspassed == true) {
			cout << "Victory! All tests for task " << tasknumber << " suceeded." << endl;		
	}
	else {
		cout << "Wrong, go back and fix task " << tasknumber << " ." << endl;
	}
}
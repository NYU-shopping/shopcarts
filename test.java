import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class test{
	public static void main(String[] args){
		// Scanner reader = null;

		// try{
  //       	reader = new Scanner(new File("input1.txt"));
	 //    }catch (FileNotFoundException e){
	 //        e.printStackTrace();
	 //    }

		// for(int i = 0; i < 4; i++){
		// 	System.out.println(reader.nextLine());
		// }
		// int i = 6;
		// switch(i){
		// 	case 3,4,5: System.out.println("less");
		// 	case 6: System.out.println("equal");
		// 	case 7, 8, 9: System.out.println("less");
		// }
		// System.out.println(4001%1000);
		// int[] i = new int[0];
		// for(int j = 0; j < i.length; j++){
		// 	System.out.println(i[j]);
		// }

		int[][] arrs = new int[3][];
		int[] arr1 = new int[]{1};
		int[] arr2 = new int[]{2, 3};
		int[] arr3 = new int[]{4, 5, 6};
		arrs[0] = arr1;
		arrs[1] = arr2;
		arrs[2] = arr3;

		for(int i = 0; i < 3; i++){
			for(int j = 0; j < arrs[i].length; j++){
				System.out.print(arrs[i][j]);
			}
			System.out.println("");
		}
	}
}
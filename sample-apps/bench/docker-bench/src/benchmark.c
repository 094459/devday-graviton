/*
**Copyright notes**

 (c) Copyright 2002 - 2020 Anatoly S. Krivitsky, Ph.D.
 All rights reserved

 Conditional permission for free use of the code
 As soon as above copyright notes are mentioned,
 the author grants a permission to any person or organization
 to use, distribute and publish this code for free
 Questions and comments may be directed to the author at
 akrivitsky@yahoo.com and akrivitsky@gmail.com

**Disclaimer of Liability**
  The user assumes all responsibility
 and risk for the use of this code "as is".
 There is no  warranty of any kind associated with the code.
 Under no circumstances, including negligence, shall the author be liable
 for any DIRECT, INDIRECT, INCIDENTAL, SPECIAL or CONSEQUENTIAL DAMAGES,
 or LOST PROFITS that result from the use or inability to use the code.
 Nor shall the author be liable for any such damages including,
 but not limited to, reliance by any person on any
 information obtained with the code
*/

 #include <math.h>
#include <time.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/timeb.h>
#include <string.h>

double x1, x2, x3, x4, x, y, z, t, t1, t2;
double e1[4], begin_time, end_time, dif_save, dif_time, whet_save, kilowhet,
       error, whet_err, percent_err;
int i, j, k, l, n1, n2, n3, n4, n6, n7, n8, n9, n10, n11, npass, max_pass, result, inner, outer,
    kount, isave, iotin;
double secndsmy(void);
void pa(double *);
void p3(double, double, double *);
void p0(void);




int main (int argc, char* argv[])
{
	npass = 0;
	max_pass = 2;
	inner = 250;
	outer = 250;
	//printf("Number of Inner Loops (suggest more than 3): ");
	//result = scanf("%d", &inner);
	//printf("Number of Outer Loops (suggest more than 1): ");
	//result = scanf("%d", &outer);
	do {
		printf("\n Pass # %d :  Outer Loop(s) %d  Inner Loop(s) %d ",
			npass + 1, outer, inner);
        printf("\n ________________________________________________________");
		kount = 0;
		begin_time = secndsmy();
		do {
			
			//initialize constannts

			t = 0.499975e0;
			t1 = 0.50025e0;
			t2 = 2.0e0;

			//set values of module weights

			isave = inner;
			n1 = 0 * inner;
			n2 = 12 * inner;
			n3 = 14 * inner;
			n4 = 345 * inner;
			n6 = 210 *  inner;
			n7 = 32 *  inner;
			n8 = 899 *  inner;
			n9 = 616  *  inner;
			n10 = 0 * inner;
			n11 = 93 * inner;

			//module 1 simple identifiers

			x1 = 1.0e0;
			x2 = x3 = x4 = -1.0e0;
			for (i = 1; i <= n1; i++)
			{
				x1 = (x1 + x2 + x3 - x4) * t;
				x2 = (x1 + x2 - x3 - x4) * t;
				x3 = (x1 - x2 + x3 + x4) * t;
				x4 = (-x1 + x2 + x3 + x4) * t;
			}

			//module 2 array elements

			e1[0] = 1.0e0;
			e1[1] = e1[2] = e1[3] = -1.0e0;
			
			for (i = 1; i <= n2; i++)
			{
				e1[0] = (e1[0] + e1[1] + e1[2] - e1[3]) * t;
				e1[1] = (e1[0] + e1[1] - e1[2] + e1[3]) * t;
				e1[2] = (e1[0] - e1[1] + e1[2] + e1[3]) * t;
				e1[3] = (-e1[0] + e1[1] + e1[2] + e1[3]) * t;

			}

			//module 3 array as a parameter

			for (i = 1; i <= n3; i++)
			           pa(e1);
			
			//module 4 condional jump

			j = 1;
			for (i = 1; i <= n4; i++)
			{
				if (j == 1) 
					j = 2;
				else 
					j = 3;

				if (j > 2) 
					j = 0;
				else 
					j = 1;

				if (j < 1) 
					j = 1;
				else 
					j = 0;
			}

			//module 5 omitted

            //module 6 integer arithmetic

			j = 1;
			k = 2;
			l = 3;

			for (i = 1; i <= n6; i++)
			{
				j = j * (k-j) * (l-k);
				k = l * k - (l-j) * k;
				l = (l-k) *  (k+j);

				e1[l-2] = j + k + l; //C arrays are zero based
				e1[k-2] = j * k * l;
			}

			//module 7 trig. functions

			x = y = 0.5e0;

			for (i = 1; i <= n7; i++)
			{
				x = t * atan(t2 * sin(x) * cos(x)/(cos(x+y) + cos(x-y) - 1.0e0));
				y = t * atan(t2 * sin(y) * cos(y)/(cos(x+y) + cos(x-y) - 1.0e0));
			}

			//module 8 procedure calls

			x = y = z = 1.0e0;

			for (i = 1; i <= n8; i++)
				p3(x, y, &z);

			//module 9 array references

			j = 1;
			k = 2;
			l = 3;

			e1[0] = 1.0e0;
			e1[1] = 2.0e0;
			e1[2] = 3.0e0;

			for (i = 1; i <= n9; i++)
				p0();
			

			//module 10 integer arithmetic

			k = 2;
			l = 3;

			for (i = 1; i <= n10; i++)
			{
				j = j + k;
				k = j + k;
				j = k - j;
				k = k - j - j;
			}
			
			//module 11 standard functions

			x = 0.75;
			for (i = 1; i <= n11; i++)
				x = sqrt(exp(log(x)/t1));

			inner = isave;
			kount++;
		} while (kount < outer);

		end_time = secndsmy();
		dif_time = end_time - begin_time;
		iotin = outer * inner;
		kilowhet = 100.0e0 * ((double) (iotin) / dif_time);
		printf("\n Elapsed time = %12.2lf seconds \n" 
			   "Whetstones = %12.2lf double precision kilowhets/second \n"
			   "iotin = %d", dif_time, kilowhet, iotin);
		
		npass++;

		if (npass < max_pass)
		{
			dif_save = dif_time;
			whet_save = kilowhet;
			inner *= max_pass;
		}

	} while (npass < max_pass);

	error = dif_time - (dif_save * ((double) max_pass));
	whet_err = whet_save - kilowhet;
	percent_err = whet_err * 100.0e0 / kilowhet;
	printf("\n ________________________________________________________");
	printf("\n Time error = %12.4le seconds "
           "\n Whet error = %12.4le kwhets/sec"
		   "\n %% error = %12.2lf %% whet error",
		   error, whet_err, percent_err);
        return 0;
	}

	void pa (double *e)
	{
		register int j;
		j = 0;
        lab:
		e[0] = (e[0] + e[1] + e[2] - e[3]) * t;
		e[1] = (e[0] + e[1] - e[2] + e[3]) * t;
		e[2] = (e[0] - e[1] + e[2] + e[3]) * t;
		e[3] = ( -e[0] + e[1] + e[2] + e[3]) * t;
		j += 1;
		if (j < 6)
			goto lab;
		return;
	}

	void p3 (double x, double y, double *z) 
	{
		x = t * (x + y);
		y = t * (x + y);
		*z = (x + y)/t2;
		return;
	}

	
	void p0 (void)
	{
		e1[j] = e1[k];
		e1[k] = e1[l];
		e1[l] = e1[j];
		return ;
	}

	double secndsmy(void)
	{
		time_t aclock_f;
		struct tm *today;
		struct timeb  tstruct;
		double ret;
		time(&aclock_f);
		today = localtime(&aclock_f);
		ftime(&tstruct);
		ret = ((double)tstruct.millitm) * 1.e-3 + (double)today->tm_sec 
			+ (double)(today->tm_min * 60)
			+ (double)(today->tm_hour*3600);
		return (ret);
	}
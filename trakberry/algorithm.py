	while True:
		tmp_ctr = tmp_ctr + 1
		#if tmp_ctr > 10000:
		#	break
		A.append(E[ptr][ctr[ptr]])
		if len(A) != len (set(A)):
			A.pop()
			ctr[ptr] = ctr[ptr] + 1
			while True:
				if ctr[ptr] <= (len(E[ptr]) - 1):
					break
				if (ctr[ptr] > (len(E[ptr])-1)) and ptr == 0:
					no_match = 1
					break
				ctr[ptr] = 0
				ptr = ptr - 1
				ctr[ptr] = ctr[ptr] + 1
				A.pop()
		else:
			ptr = ptr + 1
		if no_match == 1:
			nnoo = 1
			break
		if ptr > (qty_employee-1):
			break
	listX = zip(N,A)
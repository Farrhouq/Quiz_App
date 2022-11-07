def sort_tuples(tup):
        def sort_tuple_list(tup):
            nums = [b for (a, b) in tup]
            sorted_tuple_list = []
            while len(tup) != 0:
                least = max(nums)
                for tu_ple in tup:
                    if tu_ple[1] == least:
                        tup.remove(tu_ple)
                        nums.remove(least)
                        sorted_tuple_list.append(tu_ple)
            for _ in sorted_tuple_list:
                tup.append(_)
            return sorted_tuple_list

        def sort_tuple_list2(tup):
            nums = [b for (a, b) in tup]
            reps = {re for re in nums if nums.count(re) > 1}
            for rep in reps:
                nums = [b for (a, b) in tup]
                rep_count = nums.count(rep)
                occ1 = nums.index(rep)
                nums.reverse()
                occ2 = nums.index(rep)
                slise = tup[occ1 : len(tup) - occ2]
                slise.sort()
                tup[occ1 : len(tup) - occ2] = slise
            return tup

        tup = sort_tuple_list(sort_tuple_list2(tup))
        final_sorted = []
        nums = [b for (a, b) in tup]
        for num in nums:
            final_sorted.append(nums.index(num) + 1)
        fin = []
        for i in range(len(nums)):
            fin.append((final_sorted[i], tup[i]))
        return fin
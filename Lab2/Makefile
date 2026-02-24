CXX   = g++
FLAGS = -I. -O2

BENCHMARK_SRCS = benchmark.cpp \
                 algorithms/heap_sort/heap_sort.cpp \
                 algorithms/merge_sort/merge_sort.cpp \
                 algorithms/quick_sort/quick_sort.cpp \
                 algorithms/radix_sort/radix_sort_10.cpp \
                 algorithms/radix_sort/radix_sort_256.cpp \
                 utils/utils.cpp

ANIMATE_SRCS = generate_animated.cpp \
               algorithms/heap_sort/heap_sort_anim.cpp \
               algorithms/merge_sort/merge_sort_anim.cpp \
               algorithms/quick_sort/quick_sort_anim.cpp \
               algorithms/radix_sort/radix_sort_anim.cpp \
               utils/utils.cpp

all: benchmark animate

benchmark:
	$(CXX) $(BENCHMARK_SRCS) $(FLAGS) -o benchmark

animate:
	$(CXX) $(ANIMATE_SRCS) $(FLAGS) -o generate_animated

clean:
	del benchmark.exe generate_animated.exe

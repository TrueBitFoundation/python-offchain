
######################################INCLUDES#################################
#######################################VARS####################################
CXX=clang++
CXX?=clang++
LLVM_CONF?=llvm-config
CXX_FLAGS=$(shell $(LLVM_CONF) --cxxflags)
LD_FLAGS=-Wl,--start-group -lclangAST -lclangAnalysis -lclangBasic\
-lclangDriver -lclangEdit -lclangFrontend -lclangFrontendTool\
-lclangLex -lclangParse -lclangSema -lclangEdit -lclangASTMatchers\
-lclangRewrite -lclangRewriteFrontend -lclangStaticAnalyzerFrontend\
-lclangStaticAnalyzerCheckers -lclangStaticAnalyzerCore\
-lclangSerialization -lclangToolingCore -lclangTooling -lstdc++ -lLLVMRuntimeDyld -lm  -Wl,--end-group
LD_FLAGS+=$(shell $(LLVM_CONF) --ldflags --libs --system-libs)

#the target
TBC=TBC

EXTRA_CXX_FLAGS=-I$(shell $(LLVM_CONF) --src-root)/tools/clang/include -I$(shell $(LLVM_CONF) --obj-root)/tools/clang/include
EXTRA_LD_FLAGS=

CXX_FLAGS+=$(EXTRA_CXX_FLAGS)
LD_FLAGS+=$(EXTRA_LD_FLAGS)
######################################RULES####################################
.DEFAULT: all

.PHONY: all clean help $(TBC)

all: $(TBC)

.cpp.o:
	$(CXX) $(CXX_FLAGS) -c $< -o $@

$(TBC): $(TBC).o
	$(CXX) $^ $(LD_FLAGS) -o $@

clean:
	rm -f *.o *~ $(TBC)

deepclean:
	rm -f *.o *~ $(TBC)

help:
	@echo 'there is help.'
	@echo 'all is the defualt target.'
	@echo 'clean runs clean.'

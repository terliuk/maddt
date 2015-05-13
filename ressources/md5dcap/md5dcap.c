
#include <dcap.h>
#include <stdio.h>
#include <string.h>
#include <argp.h>
#include <openssl/evp.h>
#include <time.h>

/* argp setup *****************************************************************/ 

const char* argp_program_version="md5dcap 1.0";
const char* argp_program_bug_address = "<eike.middell@desy.de>";

static char args_doc[] = "<inputfile1> [<inputfile2> .. <inputfileN>]";
static char prog_doc[] = "md5dcap -- calculate checksums of files on dcache";

struct config
{
  int verbose;            // the -v flag 
  int debuglevel;         // argument for -d
  char* digest_type;      // argument for -t 
  int buffersize;         // argument for -b
  int nfiles;             // number of input files
  char** files;           // input file names
};

// name, key, arg, flags, doc
static struct argp_option options[] =
{
    {"verbose",    'v', 0,       0, "verbose output"},
    {"debug",      'd', "LEVEL", 0, "set the debug level of libdcap"},
    {"buffersize", 'b', "SIZE" , 0, "set the size of the read buffer"},
    {"type",       't', "TYPE" , 0, "digest type, e.g. md5 or sha1"}, // TODO add more
    {0} // SENTINEL
};

static error_t parse_opt (int key, char *arg, struct argp_state *state) {
    struct config* conf = state->input;

    switch (key) {
        case 'v':
            conf->verbose = 1;
            break;
        case 'd':
            conf->debuglevel = atoi(arg);
            break;
        case 'b':
            conf->buffersize = atoi(arg);
            break;
        case 't':
            conf->digest_type = arg;
            break;
        case ARGP_KEY_ARG:
            if (state->arg_num == 0) { // first argument
                int num_remaining_args = state->argc - state->next;
                conf->nfiles = num_remaining_args + 1;
                conf->files = (char**)malloc(conf->nfiles * sizeof(char*));
            }
            conf->files[state->arg_num] = (char*)malloc((strlen(arg)+1)*sizeof(char));
            strcpy(conf->files[state->arg_num], arg);
            break;
        case ARGP_KEY_END:
            if (state->arg_num < 1) { // require at least one input file
                argp_usage (state);
            }
            break;
        default:
            return ARGP_ERR_UNKNOWN;
    }
    return 0;
}

static struct argp argp = {options, parse_opt, args_doc, prog_doc};

/******************************************************************************/

int main(int argc, char* argv[]) {
    time_t start_time = time(NULL);

    struct config conf;
    conf.verbose = 0;
    conf.debuglevel = 0;
    conf.digest_type = "md5";
    conf.buffersize = 1024*64;

    argp_parse(&argp, argc, argv, 0, 0, &conf);


    if (conf.verbose) {
        printf("\n");
        printf("type      : %s\n", conf.digest_type);
        printf("nfiles    : %d\n", conf.nfiles);
        printf("verbose   : %d\n", conf.verbose);
        printf("debug     : %d\n", conf.debuglevel);
        printf("buffersize: %d\n", conf.buffersize);
        printf("\n");
    }

    if (conf.verbose)
        printf("configuring digest algorithms\n");
    
    // setup digest machinery
    OpenSSL_add_all_digests();
    EVP_MD_CTX mdctx;
    const EVP_MD *md = EVP_get_digestbyname(conf.digest_type);

    if (md == NULL) {
        printf("couldn't recognize digest type %s\n", conf.digest_type);
        exit(1);
    }

    // result arrays
    unsigned char** md_values = (unsigned char**)malloc(conf.nfiles * sizeof(char*));
    int* md_lenghts = (int*)malloc(conf.nfiles*sizeof(int*));

    int i, i_file;

    EVP_MD_CTX_init(&mdctx);
   
    // configure dcap debug level
    dc_setDebugLevel(conf.debuglevel); 
    
    int rc;
    char* buffer = (char*)malloc(conf.buffersize);

    for (i_file = 0; i_file < conf.nfiles; ++i_file) {
        EVP_DigestInit_ex(&mdctx, md, NULL);
        md_values[i_file] = (unsigned char*)malloc(EVP_MAX_MD_SIZE * sizeof(unsigned char));

        // read input file - plain version
        if (conf.verbose)
            printf("going to open %s. if the file is not staged this may take time\n", conf.files[i_file]);
        int input = dc_open(conf.files[i_file], O_RDONLY);

        if (input < 0) {
            if (conf.verbose)
                printf("error: cannot read file %s\n", conf.files[0]);
            strcpy(md_values[i_file], "<error>");
        }
        else {
            if (conf.verbose) {
                printf("going to read file and calculate checksum...\n");
            }
            while ( (rc = dc_read (input, buffer, conf.buffersize)) > 0) {
                EVP_DigestUpdate(&mdctx, buffer, rc);
            }

            if ((dc_close(input) != 0) && (conf.verbose)) {
                printf("error while closing the file.\n");
            }

            // calculate md5 sum
            EVP_DigestFinal_ex(&mdctx, md_values[i_file], &md_lenghts[i_file]);
            EVP_MD_CTX_cleanup(&mdctx);
        }
    }

    // print results
    if (conf.verbose)
        printf("\nDigests:\n\n");

    int maxlen = 0;
    for (i_file=0; i_file < conf.nfiles; ++i_file) {
        maxlen = md_lenghts[i_file] > maxlen ? md_lenghts[i_file] : maxlen;
    }
    for (i_file=0; i_file < conf.nfiles; ++i_file) {
        // print checksum
        for(i = 0; i < md_lenghts[i_file]; ++i) 
            printf("%02x", md_values[i_file][i]);
        // fill up with whitespaces until common length is reached
        for(i = 0; i < (maxlen - md_lenghts[i_file]) + 2; ++i)
            printf(" ");
        // print filename
        printf("%s\n", conf.files[i_file]);
    }

    // tidy up
    free(buffer); buffer=NULL;
    for (i = 0; i < conf.nfiles; i++)
        free(conf.files[i]);
    free(conf.files);
    conf.files = NULL;

    free(md_lenghts); md_lenghts = NULL;

    if (conf.verbose) {
        printf("finished after %d seconds.\n", (time(NULL) - start_time));
    }
}
